"""Admin analytics routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import User, Resume, ATSScore, UserSkill, Roadmap
from auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
def admin_stats(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    total_users = db.query(func.count(User.user_id)).scalar()
    total_resumes = db.query(func.count(Resume.resume_id)).scalar()
    avg_score = db.query(func.avg(ATSScore.total_score)).scalar() or 0

    # Score distribution
    scores = db.query(ATSScore.total_score).all()
    distribution = {"0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}
    for (s,) in scores:
        if s <= 20: distribution["0-20"] += 1
        elif s <= 40: distribution["21-40"] += 1
        elif s <= 60: distribution["41-60"] += 1
        elif s <= 80: distribution["61-80"] += 1
        else: distribution["81-100"] += 1

    # Domain popularity
    domains = db.query(Resume.selected_domain, func.count(Resume.resume_id)).filter(
        Resume.selected_domain.isnot(None)
    ).group_by(Resume.selected_domain).all()

    # Recent users
    recent = db.query(User).order_by(User.created_at.desc()).limit(10).all()

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "average_ats_score": round(avg_score, 1),
        "score_distribution": distribution,
        "domain_popularity": {d: c for d, c in domains},
        "recent_users": [{"user_id": u.user_id, "name": u.name, "email": u.email, "created_at": str(u.created_at)} for u in recent]
    }
