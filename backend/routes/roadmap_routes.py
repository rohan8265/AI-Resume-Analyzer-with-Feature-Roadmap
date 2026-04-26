"""Roadmap generation and tracking routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resume, UserSkill, Roadmap
from auth import get_current_user
from gap_analyzer import analyze_gaps
from roadmap_generator import generate_roadmap
from skill_extractor import extract_skills
from domain_skills import DOMAIN_SKILLS

router = APIRouter(prefix="/api/roadmap", tags=["Roadmap"])


@router.get("/generate")
def generate(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.resume_id == resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    domain = resume.selected_domain
    if not domain:
        raise HTTPException(status_code=400, detail="Please select a domain first")

    # Get user skills
    user_skills_db = db.query(UserSkill).filter(
        UserSkill.user_id == user.user_id, UserSkill.resume_id == resume.resume_id
    ).all()
    user_skill_names = [us.skill_name for us in user_skills_db]

    if not user_skill_names:
        ds = DOMAIN_SKILLS.get(domain, {})
        dsl = ds.get("essential", []) + ds.get("recommended", []) + ds.get("optional", [])
        extracted = extract_skills(resume.parsed_text or "", dsl)
        user_skill_names = [s["name"] for s in extracted]

    gap = analyze_gaps(user_skill_names, domain)
    roadmap_data = generate_roadmap(gap, domain)

    # Clear old roadmap
    db.query(Roadmap).filter(Roadmap.user_id == user.user_id, Roadmap.resume_id == resume.resume_id).delete()

    # Save roadmap
    saved_items = []
    for item in roadmap_data:
        rm = Roadmap(
            user_id=user.user_id,
            resume_id=resume.resume_id,
            domain=domain,
            week_number=item["week_number"],
            skill_name=item["skill_name"],
            tasks=item["tasks"],
            resources=item["resources"],
            project_idea=item["project_idea"],
            estimated_hours=item["estimated_hours"],
            is_completed=False
        )
        db.add(rm)
        saved_items.append(rm)
    db.commit()

    returned_roadmap = []
    for rm in saved_items:
        db.refresh(rm)
        returned_roadmap.append({
            "roadmap_id": rm.roadmap_id,
            "week_number": rm.week_number,
            "skill_name": rm.skill_name,
            "domain": rm.domain,
            "tasks": rm.tasks,
            "resources": rm.resources,
            "project_idea": rm.project_idea,
            "estimated_hours": rm.estimated_hours,
            "is_completed": rm.is_completed
        })

    return {"message": "Roadmap generated", "roadmap": returned_roadmap, "total_weeks": max((r["week_number"] for r in roadmap_data), default=0)}


@router.get("/{user_id}")
def get_roadmap(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.user_id != user_id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    items = db.query(Roadmap).filter(Roadmap.user_id == user_id).order_by(Roadmap.week_number).all()
    total = len(items)
    completed = sum(1 for i in items if i.is_completed)

    roadmap = [{
        "roadmap_id": i.roadmap_id,
        "week_number": i.week_number,
        "skill_name": i.skill_name,
        "domain": i.domain,
        "tasks": i.tasks,
        "resources": i.resources,
        "project_idea": i.project_idea,
        "estimated_hours": i.estimated_hours,
        "is_completed": i.is_completed
    } for i in items]

    return {
        "roadmap": roadmap,
        "total_items": total,
        "completed_items": completed,
        "progress_percentage": round((completed / max(total, 1)) * 100, 1)
    }


class CompleteWeekRequest(BaseModel):
    roadmap_id: int
    is_completed: bool = True


@router.patch("/week/complete")
def complete_week(req: CompleteWeekRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.query(Roadmap).filter(Roadmap.roadmap_id == req.roadmap_id, Roadmap.user_id == user.user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found")

    item.is_completed = req.is_completed
    db.commit()
    return {"message": "Updated", "roadmap_id": item.roadmap_id, "is_completed": item.is_completed}
