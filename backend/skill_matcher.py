"""Skill Matching — BERT cosine similarity + Jaccard similarity scoring."""
import numpy as np

_sentence_model = None

def _get_model():
    global _sentence_model
    if _sentence_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            pass
    return _sentence_model


def compute_skill_similarity(user_skills: list, domain_skills: list) -> dict:
    """Compute combined similarity: 0.7*Cosine + 0.3*Jaccard."""
    user_set = set(s.lower() for s in user_skills)
    domain_set = set(s.lower() for s in domain_skills)

    # Jaccard similarity
    intersection = user_set & domain_set
    union = user_set | domain_set
    jaccard = len(intersection) / max(len(union), 1)

    # Cosine similarity via BERT
    cosine_sim = _compute_cosine(user_skills, domain_skills)

    combined = 0.7 * cosine_sim + 0.3 * jaccard
    coverage = len(intersection) / max(len(domain_set), 1)

    # Per-skill scores
    individual_scores = {}
    for skill in domain_skills:
        if skill.lower() in user_set:
            individual_scores[skill] = 1.0
        else:
            individual_scores[skill] = _find_best_match_score(skill, user_skills)

    return {
        "combined_score": round(combined, 4),
        "cosine_similarity": round(cosine_sim, 4),
        "jaccard_similarity": round(jaccard, 4),
        "coverage_percentage": round(coverage * 100, 1),
        "individual_scores": individual_scores
    }


def _compute_cosine(user_skills, domain_skills):
    model = _get_model()
    if model is None or not user_skills or not domain_skills:
        # Fallback to keyword overlap
        u = set(s.lower() for s in user_skills)
        d = set(s.lower() for s in domain_skills)
        return len(u & d) / max(len(d), 1)

    try:
        user_emb = model.encode(user_skills, show_progress_bar=False)
        domain_emb = model.encode(domain_skills, show_progress_bar=False)
        user_mean = np.mean(user_emb, axis=0)
        domain_mean = np.mean(domain_emb, axis=0)
        cos = float(np.dot(user_mean, domain_mean) / (
            np.linalg.norm(user_mean) * np.linalg.norm(domain_mean) + 1e-8))
        return max(cos, 0)
    except Exception:
        return 0.0


def _find_best_match_score(skill, user_skills):
    model = _get_model()
    if model is None or not user_skills:
        return 0.0
    try:
        skill_emb = model.encode([skill], show_progress_bar=False)
        user_embs = model.encode(user_skills, show_progress_bar=False)
        sims = np.dot(user_embs, skill_emb.T).flatten()
        norms = np.linalg.norm(user_embs, axis=1) * np.linalg.norm(skill_emb) + 1e-8
        cosines = sims / norms
        return float(max(np.max(cosines), 0))
    except Exception:
        return 0.0
