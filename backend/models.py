from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
    ats_scores = relationship("ATSScore", back_populates="user")
    user_skills = relationship("UserSkill", back_populates="user")
    roadmaps = relationship("Roadmap", back_populates="user")


class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_format = Column(String(10), nullable=False)
    parsed_text = Column(Text)
    parsed_sections = Column(JSON)  # Structured sections data
    selected_domain = Column(String(50))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    ats_scores = relationship("ATSScore", back_populates="resume")


class ATSScore(Base):
    __tablename__ = "ats_scores"

    score_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    total_score = Column(Float, default=0.0)
    breakdown = Column(JSON)  # Section-wise scores
    suggestions = Column(JSON)  # Improvement suggestions
    scored_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ats_scores")
    resume = relationship("Resume", back_populates="ats_scores")


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    domain = Column(String(50), nullable=False)
    priority_tier = Column(String(20), nullable=False)  # essential, recommended, optional
    weight = Column(Float, nullable=False)
    difficulty = Column(String(20), default="intermediate")  # beginner, intermediate, advanced
    prerequisites = Column(JSON)  # List of prerequisite skill names


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=True)
    skill_name = Column(String(100), nullable=False)
    match_score = Column(Float, default=0.0)
    source = Column(String(50))  # ner, ontology, bert, tfidf

    user = relationship("User", back_populates="user_skills")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    roadmap_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    domain = Column(String(50), nullable=False)
    week_number = Column(Integer, nullable=False)
    skill_name = Column(String(100), nullable=False)
    tasks = Column(JSON)
    resources = Column(JSON)
    project_idea = Column(Text)
    estimated_hours = Column(Float, default=5.0)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
