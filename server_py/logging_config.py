import logging
import os
import sys

# Input budgets (characters). Text beyond these is truncated before the LLM call.
MAX_RESUME_CHARS = int(os.getenv("MAX_RESUME_CHARS", "20000"))
MAX_JD_CHARS = int(os.getenv("MAX_JD_CHARS", "10000"))
CHARS_PER_TOKEN = 4  # rough estimate for English text


def est_tokens(chars: int) -> int:
    return max(1, chars // CHARS_PER_TOKEN) if chars else 0


def setup_logging() -> logging.Logger:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)-14s | %(message)s", "%H:%M:%S")
    )
    root = logging.getLogger("resume")
    root.handlers = [handler]
    root.setLevel(level)
    root.propagate = False
    logging.getLogger("werkzeug").setLevel(logging.WARNING)  # our own request logs replace its access log
    return root


def print_startup_banner(model: str, port: str, db_url: str = "") -> None:
    log = logging.getLogger("resume.startup")
    lines = [
        "=" * 78,
        " RESUME ANALYZER BACKEND - ONLINE",
        "=" * 78,
        f" Model            : {model} (via OpenRouter)",
        f" Port             : {port}",
        " Framework        : Flask (REST API)",
        f" Database         : {db_url.split('@')[-1] if '@' in db_url else db_url}",
        " Endpoints        : POST /api/auth/signup   POST /api/auth/login   GET /api/auth/me",
        "                    POST /api/analyze (needs Bearer token)   GET /health",
        "",
        " AUTH: signup stores email + hashed password (never plain text) in the users table;",
        "       login checks the hash, updates last_login_at and returns a signed JWT;",
        "       /api/analyze rejects requests without a valid token (401).",
        "",
        " PIPELINE (each request is logged stage by stage, tagged [req-id]):",
        "  1. RECEIVE   - form data arrives: job description + resume file/text",
        "                 chars counted for JD and resume input",
        "  2. PARSE     - file_parser extracts text from .pdf/.docx/.txt",
        "                 logs: file type, bytes in, characters out, pages/paragraphs",
        "  3. BUDGET    - input size guard before the LLM call",
        f"                 resume limit = {MAX_RESUME_CHARS} chars, JD limit = {MAX_JD_CHARS} chars",
        "                 over the limit -> truncated + WARNING logged",
        "  4. LLM CALL  - one chat completion to OpenRouter",
        f"                 tokens are estimated as chars / {CHARS_PER_TOKEN}; logs prompt chars,",
        "                 est. prompt tokens, latency, response chars, provider token usage",
        "  5. PARSE JSON- LLM output validated as JSON (score, matched, missing, ...)",
        "",
        " CHUNKS & CHARACTERS - what they are used for:",
        "  - Characters : measured at RECEIVE, PARSE and BUDGET to keep the prompt inside the",
        "                 model's context window and to spot empty/scanned PDFs.",
        "  - Chunks     : resume + JD are sent as ONE chunk (single-pass, no splitting).",
        "                 Each log line shows 'chunks=1'. Oversized input is truncated, not",
        "                 split, so a resume is never scored on partial, disjoint pieces.",
        "  - Tokens     : estimated from chars for LLM cost/latency visibility.",
        "=" * 78,
    ]
    for line in lines:
        log.info(line)
