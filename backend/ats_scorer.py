"""ATS Scoring Engine — computes 0-100 score with weighted criteria."""
import re


ACTION_VERBS = [
    "achieved", "administered", "analyzed", "built", "collaborated", "conducted",
    "coordinated", "created", "delivered", "designed", "developed", "directed",
    "drove", "engineered", "established", "executed", "generated", "implemented",
    "improved", "increased", "initiated", "integrated", "launched", "led",
    "managed", "mentored", "negotiated", "optimized", "orchestrated", "organized",
    "pioneered", "planned", "produced", "reduced", "resolved", "revamped",
    "spearheaded", "streamlined", "supervised", "transformed", "utilized"
]


def compute_ats_score(parsed_sections: dict, domain: str = None, domain_skills: list = None) -> dict:
    text = parsed_sections.get("raw_text", "")
    text_lower = text.lower()

    # 1. Keyword Density (25%)
    kw_score, kw_suggestions = _score_keyword_density(text_lower, domain, domain_skills)

    # 2. Section Completeness (20%)
    sec_score, sec_suggestions = _score_section_completeness(parsed_sections)

    # 3. Formatting & Readability (15%)
    fmt_score, fmt_suggestions = _score_formatting(text)

    # 4. Action Verbs (10%)
    verb_score, verb_suggestions = _score_action_verbs(text_lower, parsed_sections)

    # 5. Quantifiable Achievements (10%)
    quant_score, quant_suggestions = _score_quantifiable(text)

    # 6. Skill-to-Domain Match (20%)
    match_score, match_suggestions = _score_skill_match(parsed_sections, domain_skills)

    breakdown = {
        "keyword_density": {"score": round(kw_score, 1), "max": 25, "label": "Keyword Density"},
        "section_completeness": {"score": round(sec_score, 1), "max": 20, "label": "Section Completeness"},
        "formatting": {"score": round(fmt_score, 1), "max": 15, "label": "Formatting & Readability"},
        "action_verbs": {"score": round(verb_score, 1), "max": 10, "label": "Action Verbs"},
        "quantifiable": {"score": round(quant_score, 1), "max": 10, "label": "Quantifiable Achievements"},
        "skill_match": {"score": round(match_score, 1), "max": 20, "label": "Skill-to-Domain Match"},
    }

    total = sum(v["score"] for v in breakdown.values())
    suggestions = kw_suggestions + sec_suggestions + fmt_suggestions + verb_suggestions + quant_suggestions + match_suggestions

    return {
        "total_score": round(min(total, 100), 1),
        "breakdown": breakdown,
        "suggestions": suggestions
    }


def _score_keyword_density(text, domain, domain_skills):
    score = 0
    suggestions = []
    if not domain_skills:
        # Generic keyword check
        generic_kw = ["experience", "skills", "education", "project", "team", "developed", "managed"]
        found = sum(1 for kw in generic_kw if kw in text)
        score = min((found / len(generic_kw)) * 25, 25)
        if score < 15:
            suggestions.append("Add more domain-relevant keywords to your resume")
        return score, suggestions

    found = sum(1 for s in domain_skills if s.lower() in text)
    ratio = found / max(len(domain_skills), 1)
    score = min(ratio * 50, 25)  # Scale: 50% coverage = full score
    if score < 15:
        suggestions.append(f"Include more {domain} keywords — only {found}/{len(domain_skills)} found")
    return score, suggestions


def _score_section_completeness(sections):
    score = 0
    suggestions = []
    checks = {
        "personal_details": (3, "Add complete contact information (email, phone, LinkedIn)"),
        "education": (3, "Add your education details with degree, institution, and year"),
        "skills": (3, "Add a comprehensive skills section"),
        "work_experience": (4, "Include detailed work experience with descriptions"),
        "projects": (3, "Add projects to showcase your practical skills"),
        "certifications": (2, "Add certifications to boost credibility"),
        "achievements": (2, "Include achievements and awards"),
    }
    for key, (pts, suggestion) in checks.items():
        data = sections.get(key)
        if data:
            if isinstance(data, list) and len(data) > 0:
                score += pts
            elif isinstance(data, dict):
                filled = sum(1 for v in data.values() if v and v != [])
                if filled > 0:
                    score += pts
                else:
                    suggestions.append(suggestion)
            else:
                suggestions.append(suggestion)
        else:
            suggestions.append(suggestion)
    return min(score, 20), suggestions


def _score_formatting(text):
    score = 15
    suggestions = []
    lines = text.split("\n")

    # Check for very long lines (bad formatting)
    long_lines = sum(1 for l in lines if len(l) > 120)
    if long_lines > 5:
        score -= 3
        suggestions.append("Break long paragraphs into bullet points for better readability")

    # Check for consistent structure
    if len(lines) < 15:
        score -= 4
        suggestions.append("Resume appears too short — add more detail")

    # Check for excessive blank lines
    blank = sum(1 for l in lines if not l.strip())
    if blank > len(lines) * 0.4:
        score -= 2
        suggestions.append("Remove excessive blank lines for cleaner formatting")

    # Check for all-caps sections (good for headers)
    caps_lines = sum(1 for l in lines if l.strip().isupper() and len(l.strip()) > 3)
    if caps_lines < 2:
        score -= 2
        suggestions.append("Use clear section headers (EDUCATION, EXPERIENCE, etc.)")

    return max(score, 0), suggestions


def _score_action_verbs(text, sections):
    score = 0
    suggestions = []
    exp = sections.get("work_experience", [])
    exp_text = " ".join(e.get("description", e.get("raw", "")) for e in exp).lower() if exp else text

    found_verbs = [v for v in ACTION_VERBS if v in exp_text]
    ratio = len(found_verbs) / max(len(ACTION_VERBS) * 0.2, 1)
    score = min(ratio * 10, 10)

    if score < 6:
        suggestions.append(
            "Use more action verbs in experience section (e.g., 'Developed', 'Implemented', 'Led', 'Optimized')"
        )
    return score, suggestions


def _score_quantifiable(text):
    score = 0
    suggestions = []
    numbers = re.findall(r'\d+%|\d+\+|\$\d+|\d{2,}', text)
    count = len(numbers)

    if count >= 5:
        score = 10
    elif count >= 3:
        score = 7
    elif count >= 1:
        score = 4
    else:
        score = 1

    if score < 7:
        suggestions.append("Add quantifiable results (e.g., 'Increased sales by 30%', 'Managed team of 12')")
    return score, suggestions


def _score_skill_match(sections, domain_skills):
    if not domain_skills:
        return 10, ["Select a domain to get skill-match scoring"]

    user_skills = []
    sk = sections.get("skills", {})
    if isinstance(sk, dict):
        user_skills = [s.lower() for s in sk.get("technical", []) + sk.get("soft", [])]
    
    # Also check full text for skills
    text = sections.get("raw_text", "").lower()

    matched = sum(1 for s in domain_skills if s.lower() in text or s.lower() in user_skills)
    ratio = matched / max(len(domain_skills), 1)
    score = min(ratio * 40, 20)
    suggestions = []
    if score < 12:
        suggestions.append("Your skills don't closely match the target domain — review required skills")
    return score, suggestions
