import io
import logging

from errors import ApiError
from pypdf import PdfReader
from docx import Document

log = logging.getLogger("resume.parser")


def extract_text(filename: str, content: bytes, rid: str = "-") -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        text = _extract_pdf(content)
    elif name.endswith(".docx"):
        text = _extract_docx(content)
    elif name.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    else:
        log.warning("[%s] PARSE unsupported file type: %s", rid, filename)
        raise ApiError(400, "Unsupported file type. Use .pdf, .docx, or .txt")

    log.info("[%s] PARSE %s: %d bytes in -> %d chars out", rid, filename, len(content), len(text))
    return text


def _extract_pdf(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        log.info("PDF has %d page(s)", len(reader.pages))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise ApiError(400, f"Failed to read PDF: {exc}")

    if not text.strip():
        raise ApiError(400, "No extractable text found in PDF (it may be scanned/image-based).")
    return text


def _extract_docx(content: bytes) -> str:
    try:
        doc = Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs)
    except Exception as exc:
        raise ApiError(400, f"Failed to read DOCX: {exc}")

    if not text.strip():
        raise ApiError(400, "No extractable text found in DOCX.")
    return text
