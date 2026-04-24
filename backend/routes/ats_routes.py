"""ATS scoring routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resume, ATSScore
from auth import get_current_user
from ats_scorer import compute_ats_score
from domain_skills import DOMAIN_SKILLS

router = APIRouter(prefix="/api/ats", tags=["ATS Score"])


class ScoreRequest(BaseModel):
    resume_id: int


@router.post("/score")
def score_resume(req: ScoreRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.resume_id == req.resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Get domain skills if domain is selected
    domain = resume.selected_domain
    domain_skill_list = []
    if domain and domain in DOMAIN_SKILLS:
        ds = DOMAIN_SKILLS[domain]
        domain_skill_list = ds.get("essential", []) + ds.get("recommended", []) + ds.get("optional", [])

    sections = resume.parsed_sections or {}
    result = compute_ats_score(sections, domain, domain_skill_list)

    # Save score
    ats = ATSScore(
        user_id=user.user_id,
        resume_id=resume.resume_id,
        total_score=result["total_score"],
        breakdown=result["breakdown"],
        suggestions=result["suggestions"]
    )
    db.add(ats)
    db.commit()
    db.refresh(ats)

    return {
        "score_id": ats.score_id,
        "total_score": result["total_score"],
        "breakdown": result["breakdown"],
        "suggestions": result["suggestions"]
    }


@router.get("/history/{resume_id}")
def score_history(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    scores = db.query(ATSScore).filter(
        ATSScore.user_id == user.user_id
    ).order_by(ATSScore.scored_at.asc()).all()
    return [{
        "score_id": s.score_id,
        "resume_id": s.resume_id,
        "total_score": s.total_score,
        "breakdown": s.breakdown,
        "scored_at": str(s.scored_at)
    } for s in scores]
