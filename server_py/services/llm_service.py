import json
import logging
import os
import re
import time

from errors import ApiError
from openai import OpenAI

from logging_config import est_tokens

log = logging.getLogger("resume.llm")

_client: OpenAI | None = None

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ApiError(500, "OPENROUTER_API_KEY is not configured on the server.")
        _client = OpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
                "X-Title": "Resume Analyzer",
            },
        )
    return _client


MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")

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


def analyze(resume_text: str, job_description: str, rid: str = "-") -> dict:
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

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    prompt_chars = len(SYSTEM_PROMPT) + len(user_prompt)
    log.info(
        "[%s] LLM CALL model=%s prompt=%d chars (~%d tokens), chunks=1",
        rid, MODEL, prompt_chars, est_tokens(prompt_chars),
    )
    start = time.perf_counter()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=messages,
            temperature=0.3,
        )
        _check_response_error(response)
    except ApiError:
        raise
    except Exception as first_exc:
        # Some OpenRouter models (esp. free tier) reject response_format — retry without it.
        log.warning("[%s] LLM CALL json mode failed (%s), retrying without response_format", rid, first_exc)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.3,
            )
            _check_response_error(response)
        except ApiError:
            raise
        except Exception as exc:
            raise ApiError(502, f"LLM request failed: {exc}")

    raw = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    log.info(
        "[%s] LLM DONE %.1fs response=%d chars, provider tokens: prompt=%s completion=%s",
        rid, time.perf_counter() - start, len(raw),
        getattr(usage, "prompt_tokens", "n/a"), getattr(usage, "completion_tokens", "n/a"),
    )
    raw = _strip_code_fence(raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        log.error("[%s] PARSE JSON failed, LLM output was not valid JSON", rid)
        raise ApiError(502, "LLM returned invalid JSON.")

    log.info(
        "[%s] PARSE JSON ok score=%s matched=%d missing=%d",
        rid, data.get("score"), len(data.get("matched", [])), len(data.get("missing", [])),
    )
    return data


def _check_response_error(response) -> None:
    error = getattr(response, "error", None)
    if error:
        message = error.get("message", str(error)) if isinstance(error, dict) else str(error)
        raise ApiError(503, f"Model provider error: {message}")
    if not response.choices:
        raise ApiError(502, "LLM returned no response choices.")


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    return match.group(1) if match else text
