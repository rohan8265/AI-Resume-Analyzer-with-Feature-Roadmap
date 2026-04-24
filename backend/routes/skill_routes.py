"""Skill extraction, gap analysis, and domain selection routes."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import User, Resume, UserSkill, Skill
from auth import get_current_user
from skill_extractor import extract_skills
from skill_matcher import compute_skill_similarity
from gap_analyzer import analyze_gaps
from domain_skills import DOMAIN_SKILLS

router = APIRouter(prefix="/api", tags=["Skills"])

DOMAINS = list(DOMAIN_SKILLS.keys())


class DomainSelectRequest(BaseModel):
    resume_id: int
    domain: str


@router.get("/domains")
def list_domains():
    return {"domains": DOMAINS}


@router.post("/domain/select")
def select_domain(req: DomainSelectRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if req.domain not in DOMAIN_SKILLS:
        raise HTTPException(status_code=400, detail=f"Invalid domain. Choose from: {DOMAINS}")

    resume = db.query(Resume).filter(Resume.resume_id == req.resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.selected_domain = req.domain
    db.commit()
    return {"message": f"Domain set to {req.domain}", "domain": req.domain}


@router.get("/skills/extracted")
def get_extracted_skills(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.resume_id == resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    domain = resume.selected_domain
    if not domain:
        raise HTTPException(status_code=400, detail="Please select a domain first")

    ds = DOMAIN_SKILLS.get(domain, {})
    domain_skill_list = ds.get("essential", []) + ds.get("recommended", []) + ds.get("optional", [])

    # Extract skills
    text = resume.parsed_text or ""
    extracted = extract_skills(text, domain_skill_list)

    # Clear old user skills for this resume
    db.query(UserSkill).filter(UserSkill.user_id == user.user_id, UserSkill.resume_id == resume.resume_id).delete()

    # Save new skills
    for skill_data in extracted:
        us = UserSkill(
            user_id=user.user_id,
            resume_id=resume.resume_id,
            skill_name=skill_data["name"],
            match_score=skill_data["score"],
            source=skill_data["source"]
        )
        db.add(us)
    db.commit()

    # Compute similarity
    user_skill_names = [s["name"] for s in extracted]
    similarity = compute_skill_similarity(user_skill_names, domain_skill_list)

    return {
        "extracted_skills": extracted,
        "similarity": similarity,
        "domain": domain,
        "total_domain_skills": len(domain_skill_list)
    }


@router.get("/skills/gap")
def get_skill_gap(resume_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.resume_id == resume_id, Resume.user_id == user.user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    domain = resume.selected_domain
    if not domain:
        raise HTTPException(status_code=400, detail="Please select a domain first")

    # Get user skills
    user_skills_db = db.query(UserSkill).filter(
        UserSkill.user_id == user.user_id,
        UserSkill.resume_id == resume.resume_id
    ).all()

    user_skill_names = [us.skill_name for us in user_skills_db]

    # If no skills extracted yet, extract them first
    if not user_skill_names:
        ds = DOMAIN_SKILLS.get(domain, {})
        domain_skill_list = ds.get("essential", []) + ds.get("recommended", []) + ds.get("optional", [])
        extracted = extract_skills(resume.parsed_text or "", domain_skill_list)
        user_skill_names = [s["name"] for s in extracted]

    gap = analyze_gaps(user_skill_names, domain)
    return gap
