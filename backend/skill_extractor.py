"""NLP Skill Extraction — spaCy NER + Ontology Matching + Sentence-BERT + TF-IDF."""
import re
import numpy as np
from rapidfuzz import fuzz
from config import BERT_SIMILARITY_THRESHOLD, FUZZY_MATCH_THRESHOLD

# Lazy-loaded globals
_nlp = None
_sentence_model = None
_tfidf_vectorizer = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            _nlp = None
    return _nlp


def _get_sentence_model():
    global _sentence_model
    if _sentence_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            _sentence_model = None
    return _sentence_model


def extract_skills(resume_text: str, domain_skills: list) -> list:
    """Hybrid skill extraction pipeline."""
    extracted = {}

    # Step 1: spaCy NER extraction
    ner_skills = _spacy_extract(resume_text)
    for skill in ner_skills:
        extracted[skill.lower()] = {"name": skill, "score": 0.8, "source": "ner"}

    # Step 2: Ontology matching (exact + fuzzy)
    onto_skills = _ontology_match(resume_text, domain_skills)
    for skill, score in onto_skills:
        key = skill.lower()
        if key not in extracted or extracted[key]["score"] < score:
            extracted[key] = {"name": skill, "score": score, "source": "ontology"}

    # Step 3: Sentence-BERT embedding match
    bert_skills = _bert_match(resume_text, domain_skills)
    for skill, score in bert_skills:
        key = skill.lower()
        if key not in extracted or extracted[key]["score"] < score:
            extracted[key] = {"name": skill, "score": score, "source": "bert"}

    # Step 4: TF-IDF fallback
    tfidf_skills = _tfidf_match(resume_text, domain_skills)
    for skill, score in tfidf_skills:
        key = skill.lower()
        if key not in extracted:
            extracted[key] = {"name": skill, "score": score, "source": "tfidf"}

    return list(extracted.values())


def _spacy_extract(text: str) -> list:
    """Use spaCy to extract potential skill entities."""
    nlp = _get_nlp()
    if nlp is None:
        return []

    doc = nlp(text)
    skills = []

    # Extract noun chunks that could be skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if 1 < len(chunk_text) < 50 and not chunk_text[0].isdigit():
            skills.append(chunk_text)

    # Extract named entities
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT", "WORK_OF_ART", "EVENT"):
            skills.append(ent.text.strip())

    return skills


def _ontology_match(text: str, domain_skills: list) -> list:
    """Exact and fuzzy match against domain skill library."""
    text_lower = text.lower()
    matched = []

    for skill in domain_skills:
        # Exact match
        if skill.lower() in text_lower:
            matched.append((skill, 1.0))
            continue

        # Fuzzy match against text segments
        words = text_lower.split()
        # Check bigrams and trigrams
        for n in [1, 2, 3]:
            for i in range(len(words) - n + 1):
                segment = " ".join(words[i:i+n])
                ratio = fuzz.ratio(skill.lower(), segment)
                if ratio >= FUZZY_MATCH_THRESHOLD:
                    matched.append((skill, ratio / 100.0))
                    break
            else:
                continue
            break

    return matched


def _bert_match(text: str, domain_skills: list) -> list:
    """Use Sentence-BERT to detect implicit skills."""
    model = _get_sentence_model()
    if model is None:
        return []

    matched = []
    try:
        # Split resume into sentences
        sentences = [s.strip() for s in re.split(r'[.\n]', text) if len(s.strip()) > 10]
        if not sentences:
            return []

        # Encode
        sent_embeddings = model.encode(sentences[:50], show_progress_bar=False)
        skill_embeddings = model.encode(domain_skills, show_progress_bar=False)

        # Compute similarities
        for i, skill_emb in enumerate(skill_embeddings):
            sims = np.dot(sent_embeddings, skill_emb) / (
                np.linalg.norm(sent_embeddings, axis=1) * np.linalg.norm(skill_emb) + 1e-8
            )
            max_sim = float(np.max(sims))
            if max_sim >= BERT_SIMILARITY_THRESHOLD:
                matched.append((domain_skills[i], max_sim))
    except Exception:
        pass

    return matched


def _tfidf_match(text: str, domain_skills: list) -> list:
    """TF-IDF based matching as fallback."""
    matched = []
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        corpus = [text] + domain_skills
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)

        sims = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        for i, sim in enumerate(sims):
            if sim >= 0.1:
                matched.append((domain_skills[i], float(sim)))
    except Exception:
        pass

    return matched
