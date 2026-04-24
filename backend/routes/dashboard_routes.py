"""Dashboard data route — aggregates all user data."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resume, ATSScore, UserSkill, Roadmap
from auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.user_id != user_id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    # Resumes
    resumes = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.uploaded_at.desc()).all()
    resume_data = [{
        "resume_id": r.resume_id, "filename": r.filename, "file_format": r.file_format,
        "uploaded_at": str(r.uploaded_at), "selected_domain": r.selected_domain,
        "parsed_sections": r.parsed_sections
    } for r in resumes]

    # ATS Scores
    scores = db.query(ATSScore).filter(ATSScore.user_id == user_id).order_by(ATSScore.scored_at.asc()).all()
    score_data = [{
        "score_id": s.score_id, "resume_id": s.resume_id, "total_score": s.total_score,
        "breakdown": s.breakdown, "suggestions": s.suggestions, "scored_at": str(s.scored_at)
    } for s in scores]

    # Skills
    skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    skill_data = [{
        "skill_name": s.skill_name, "match_score": s.match_score, "source": s.source
    } for s in skills]

    # Roadmap
    roadmap_items = db.query(Roadmap).filter(Roadmap.user_id == user_id).order_by(Roadmap.week_number).all()
    roadmap_data = [{
        "roadmap_id": r.roadmap_id, "week_number": r.week_number, "skill_name": r.skill_name,
        "domain": r.domain, "tasks": r.tasks, "resources": r.resources,
        "project_idea": r.project_idea, "estimated_hours": r.estimated_hours,
        "is_completed": r.is_completed
    } for r in roadmap_items]

    total_rm = len(roadmap_items)
    completed_rm = sum(1 for r in roadmap_items if r.is_completed)

    return {
        "user": {"user_id": user_id, "name": user.name, "email": user.email},
        "resumes": resume_data,
        "ats_scores": score_data,
        "latest_score": score_data[-1] if score_data else None,
        "skills": skill_data,
        "roadmap": roadmap_data,
        "roadmap_progress": {
            "total": total_rm, "completed": completed_rm,
            "percentage": round((completed_rm / max(total_rm, 1)) * 100, 1)
        }
    }
