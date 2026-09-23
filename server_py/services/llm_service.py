import json
import os

from fastapi import HTTPException
from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured on the server.")
        _client = OpenAI(api_key=api_key)
    return _client


MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach acting as an AI resume evaluation agent.
Given a candidate's resume text and a target job description, you must:

1. Judge the genuine fit between the resume and the job description (skills, experience, relevance) — do not just
   pattern-match keywords, reason about actual competency signals in the resume text.
2. Produce an overall match score from 0-100.
3. List the skills/requirements from the job description that the candidate demonstrably matches.
4. List the skills/requirements from the job description that are missing or weakly evidenced in the resume.
5. For up to 6 of the most important job-relevant skills, rate the candidate's demonstrated strength in each
   from 0-100 (skillBars).
6. For up to 4 of the most important missing skills, act as a career coach and provide a concrete, ordered
   recommended learning path (3-4 actionable, specific steps — not generic advice) the candidate could follow to
   close that gap, referencing realistic resources/approaches (e.g. specific certification types, project ideas,
   practice methods) tailored to that skill.
7. Write a short (2-3 sentence) summary explaining the overall fit and reasoning.

Respond ONLY with strict JSON matching exactly this shape, no markdown, no commentary:
{
  "score": <int 0-100>,
  "summary": "<string>",
  "matched": ["<string>", ...],
  "missing": ["<string>", ...],
  "skillBars": [{"skill": "<string>", "score": <int 0-100>}, ...],
  "enhance": [{"skill": "<string>", "tips": ["<string>", "<string>", "<string>"]}, ...]
}
"""


def analyze(resume_text: str, job_description: str) -> dict:
    client = _get_client()

    user_prompt = f"""RESUME:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {exc}")

    raw = response.choices[0].message.content
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="LLM returned invalid JSON.")

    return data
