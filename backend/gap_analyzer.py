"""Skill Gap Analysis — compares user skills against domain requirements."""
from domain_skills import DOMAIN_SKILLS


def analyze_gaps(user_skills: list, domain: str) -> dict:
    """Identify matched and missing skills by priority tier."""
    domain_data = DOMAIN_SKILLS.get(domain, {})
    user_skill_names = set(s.lower() for s in user_skills)

    result = {"matched": [], "missing_essential": [], "missing_recommended": [], "missing_optional": []}
    coverage = {"essential": 0, "recommended": 0, "optional": 0}
    totals = {"essential": 0, "recommended": 0, "optional": 0}

    for tier in ["essential", "recommended", "optional"]:
        skills = domain_data.get(tier, [])
        totals[tier] = len(skills)
        for skill in skills:
            if skill.lower() in user_skill_names:
                result["matched"].append({"name": skill, "tier": tier})
                coverage[tier] += 1
            else:
                result[f"missing_{tier}"].append({"name": skill, "tier": tier})

    result["coverage"] = {
        tier: round((coverage[tier] / max(totals[tier], 1)) * 100, 1)
        for tier in ["essential", "recommended", "optional"]
    }
    result["overall_coverage"] = round(
        (sum(coverage.values()) / max(sum(totals.values()), 1)) * 100, 1
    )
    result["totals"] = totals
    result["matched_counts"] = coverage

    return result
