import os

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_analyzer.db")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "ai-resume-analyzer-secret-key-change-in-production-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Upload
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FAISS
FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
os.makedirs(FAISS_INDEX_PATH, exist_ok=True)

# Model
SENTENCE_MODEL_NAME = "all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"

# Similarity thresholds
BERT_SIMILARITY_THRESHOLD = 0.75
FUZZY_MATCH_THRESHOLD = 80

# Performance Mode
# Set FAST_MODE to True to disable heavy ML models (BERT/spaCy) for faster local and deployed performance.
FAST_MODE = os.getenv("FAST_MODE", "True").lower() in ("true", "1", "yes")
