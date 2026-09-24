import logging

from flask import Blueprint, g, jsonify, request

from errors import ApiError
from logging_config import MAX_JD_CHARS, MAX_RESUME_CHARS, est_tokens
from models.schemas import AnalysisResult
from services.auth_service import login_required
from services.file_parser import extract_text
from services.llm_service import analyze

bp = Blueprint("analyze", __name__)
log = logging.getLogger("resume.analyze")


def _budget(label: str, text: str, limit: int, rid: str) -> str:
    n = len(text)
    if n > limit:
        log.warning("[%s] BUDGET %s %d chars > limit %d -> truncated (lost %d chars)", rid, label, n, limit, n - limit)
        return text[:limit]
    log.info("[%s] BUDGET %s %d/%d chars OK", rid, label, n, limit)
    return text


@bp.post("/analyze")
@login_required
def analyze_resume():
    rid = g.req_id
    job_description = request.form.get("job_description", "")
    resume_text = request.form.get("resume_text") or ""
    resume_file = request.files.get("resume_file")

    if not job_description.strip():
        raise ApiError(400, "job_description is required.")

    log.info(
        "[%s] RECEIVE user=%s jd=%d chars, resume_file=%s, resume_text=%d chars",
        rid, g.user.email, len(job_description), resume_file.filename if resume_file else None, len(resume_text),
    )

    if resume_file is not None and resume_file.filename:
        text = extract_text(resume_file.filename, resume_file.read(), rid)
    elif resume_text.strip():
        text = resume_text
        log.info("[%s] PARSE pasted text, no extraction needed (%d chars)", rid, len(text))
    else:
        raise ApiError(400, "Provide either resume_file or resume_text.")

    text = _budget("resume", text, MAX_RESUME_CHARS, rid)
    jd = _budget("job_description", job_description, MAX_JD_CHARS, rid)
    log.info(
        "[%s] BUDGET total=%d chars (~%d tokens), chunks=1 (single-pass)",
        rid, len(text) + len(jd), est_tokens(len(text) + len(jd)),
    )

    result = analyze(text, jd, rid)
    try:
        return jsonify(AnalysisResult.model_validate(result).model_dump())
    except Exception:
        log.error("[%s] LLM JSON did not match the expected schema", rid)
        raise ApiError(502, "LLM returned an unexpected response shape.")
