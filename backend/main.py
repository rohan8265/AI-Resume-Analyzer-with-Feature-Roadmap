"""AI Resume Analyzer — FastAPI Backend Entry Point."""
import traceback
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes.auth_routes import router as auth_router
from routes.resume_routes import router as resume_router
from routes.ats_routes import router as ats_router
from routes.skill_routes import router as skill_router
from routes.roadmap_routes import router as roadmap_router
from routes.dashboard_routes import router as dashboard_router
from routes.admin_routes import router as admin_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume Analyzer",
    description="Intelligent career tech platform with ATS scoring, skill gap analysis, and personalized roadmaps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    logger.error(f"Unhandled exception: {exc}\n{tb}")
    print(f"ERROR: {exc}\n{tb}", flush=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


# Register routes
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(skill_router)
app.include_router(roadmap_router)
app.include_router(dashboard_router)
app.include_router(admin_router)


@app.on_event("startup")
def startup():
    init_db()
    
    # Create default admin
    from database import SessionLocal
    from models import User
    from auth import hash_password
    
    db = SessionLocal()
    admin_email = "guptarohan91924@gmail.com"
    user = db.query(User).filter(User.email == admin_email).first()
    
    if not user:
        user = User(
            name="Admin Rohan",
            email=admin_email,
            password_hash=hash_password("123455"),
            is_admin=True
        )
        db.add(user)
    else:
        user.is_admin = True
        user.password_hash = hash_password("123455")
        
    db.commit()
    db.close()


@app.get("/")
def root():
    return {"message": "AI Resume Analyzer API", "docs": "/docs"}
