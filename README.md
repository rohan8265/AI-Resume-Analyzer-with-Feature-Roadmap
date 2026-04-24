# AI Resume Analyzer with Feature Roadmap

An intelligent career tech platform that analyzes resumes, computes ATS scores, extracts skills using NLP, identifies skill gaps, and generates personalized weekly learning roadmaps.

## Tech Stack

- **Frontend**: React.js + Tailwind CSS + Recharts (Vite)
- **Backend**: Python FastAPI
- **NLP**: spaCy, Sentence-Transformers (BERT), TF-IDF, rapidfuzz
- **Database**: SQLite (default) / PostgreSQL + FAISS
- **Auth**: JWT with bcrypt password hashing

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py             # Configuration
│   ├── database.py           # SQLAlchemy setup
│   ├── models.py             # ORM models
│   ├── auth.py               # JWT authentication
│   ├── resume_parser.py      # PDF/DOCX/TXT parsing
│   ├── ats_scorer.py         # ATS scoring engine
│   ├── skill_extractor.py    # Hybrid NLP extraction
│   ├── skill_matcher.py      # BERT + Jaccard similarity
│   ├── gap_analyzer.py       # Skill gap analysis
│   ├── roadmap_generator.py  # Weekly roadmap generation
│   ├── domain_skills.py      # 1200+ skills across 7 domains
│   ├── requirements.txt
│   └── routes/
│       ├── auth_routes.py
│       ├── resume_routes.py
│       ├── ats_routes.py
│       ├── skill_routes.py
│       ├── roadmap_routes.py
│       ├── dashboard_routes.py
│       └── admin_routes.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── context/AuthContext.jsx
        ├── services/api.js
        ├── components/
        │   ├── Navbar.jsx
        │   ├── ATSGauge.jsx
        │   ├── SkillGapChart.jsx
        │   └── RoadmapView.jsx
        └── pages/
            ├── LandingPage.jsx
            ├── LoginPage.jsx
            ├── RegisterPage.jsx
            ├── UploadPage.jsx
            ├── AnalysisPage.jsx
            ├── DashboardPage.jsx
            └── AdminPage.jsx
```

## Setup & Run

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install Node.js if not installed: https://nodejs.org/

# Install dependencies
npm install

# Run dev server
npm run dev
```

The app will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features

1. **User Authentication** - Register/Login with JWT
2. **Resume Upload** - PDF, DOCX, TXT support
3. **Resume Parsing** - Extracts sections (education, skills, experience, etc.)
4. **ATS Scoring** - 0-100 score with 6 weighted criteria
5. **Domain Selection** - 7 career domains with 1200+ skills
6. **NLP Skill Extraction** - spaCy NER + Ontology + BERT + TF-IDF
7. **Skill Gap Analysis** - Essential/Recommended/Optional tiers
8. **Learning Roadmap** - 8-24 week personalized plan
9. **Progress Tracking** - Score trends and roadmap completion
10. **Admin Panel** - User analytics and score distributions

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login, return JWT |
| POST | /api/resume/upload | Upload & parse resume |
| GET | /api/resume/:id | Get parsed resume |
| POST | /api/ats/score | Compute ATS score |
| POST | /api/domain/select | Set target domain |
| GET | /api/skills/extracted | Get extracted skills |
| GET | /api/skills/gap | Get skill gap analysis |
| GET | /api/roadmap/generate | Generate roadmap |
| GET | /api/roadmap/:user_id | Get full roadmap |
| PATCH | /api/roadmap/week/complete | Mark week complete |
| GET | /api/dashboard/:user_id | Full dashboard data |
| GET | /api/admin/stats | Admin analytics |
