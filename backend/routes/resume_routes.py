"""Resume upload and retrieval routes."""
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resume
from auth import get_current_user
from resume_parser import extract_text, parse_sections
from config import UPLOAD_DIR

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Validate format
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ("pdf", "docx", "txt"):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are accepted")

    file_bytes = await file.read()

    # Save file
    filepath = os.path.join(UPLOAD_DIR, f"{user.user_id}_{file.filename}")
    with open(filepath, "wb") as f:
        f.write(file_bytes)

    # Extract and parse
    raw_text = extract_text(file_bytes, ext)
    sections = parse_sections(raw_text)

    resume = Resume(
        user_id=user.user_id,
        filename=file.filename,
        file_format=ext,
        parsed_text=raw_text,
        parsed_sections=sections
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded and parsed successfully",
        "resume_id": resume.resume_id,
        "filename": resume.filename,
        "sections": sections
    }


@router.get("/list")
def list_resumes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resumes = db.query(Resume).filter(Resume.user_id == user.user_id).order_by(Resume.uploaded_at.desc()).all()
    return [{
        "resume_id": r.resume_id,
        "filename": r.filename,
        "file_format": r.file_format,
        "uploaded_at": str(r.uploaded_at),
        "selected_domain": r.selected_domain
    } for r in resumes]


@router.get("/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.resume_id == resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {
        "resume_id": resume.resume_id,
        "filename": resume.filename,
        "file_format": resume.file_format,
        "uploaded_at": str(resume.uploaded_at),
        "parsed_sections": resume.parsed_sections,
        "selected_domain": resume.selected_domain
    }
