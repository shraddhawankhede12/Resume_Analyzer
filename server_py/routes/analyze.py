from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.schemas import AnalysisResult
from services.file_parser import extract_text
from services.llm_service import analyze

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_resume(
    job_description: str = Form(...),
    resume_text: str | None = Form(None),
    resume_file: UploadFile | None = File(None),
):
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required.")

    if resume_file is not None:
        content = await resume_file.read()
        text = extract_text(resume_file.filename, content)
    elif resume_text and resume_text.strip():
        text = resume_text
    else:
        raise HTTPException(status_code=400, detail="Provide either resume_file or resume_text.")

    result = analyze(text, job_description)
    return result
