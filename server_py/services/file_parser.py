import io

from fastapi import HTTPException
from pypdf import PdfReader
from docx import Document


def extract_text(filename: str, content: bytes) -> str:
    name = filename.lower()

    if name.endswith(".pdf"):
        return _extract_pdf(content)
    if name.endswith(".docx"):
        return _extract_docx(content)
    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    raise HTTPException(status_code=400, detail="Unsupported file type. Use .pdf, .docx, or .txt")


def _extract_pdf(content: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {exc}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in PDF (it may be scanned/image-based).")
    return text


def _extract_docx(content: bytes) -> str:
    try:
        doc = Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read DOCX: {exc}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in DOCX.")
    return text
