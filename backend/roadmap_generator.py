"""Roadmap Generator — creates personalized 8-24 week learning plans."""
from domain_skills import SKILL_PREREQUISITES, SKILL_DIFFICULTY, LEARNING_RESOURCES, DEFAULT_RESOURCES, DOMAIN_SKILLS


def generate_roadmap(gap_analysis: dict, domain: str) -> list:
    """Generate weekly roadmap from gap analysis results."""
    missing_essential = gap_analysis.get("missing_essential", [])
    missing_recommended = gap_analysis.get("missing_recommended", [])
    missing_optional = gap_analysis.get("missing_optional", [])

    # Determine duration
    n_essential = len(missing_essential)
    if n_essential <= 5:
        total_weeks = 8
    elif n_essential <= 10:
        total_weeks = 12
    else:
        total_weeks = min(16 + (n_essential - 11), 24)

    # Build priority-sorted skill list
    all_missing = []
    weights = {"essential": 0.6, "recommended": 0.3, "optional": 0.1}
    for tier, skills in [("essential", missing_essential), ("recommended", missing_recommended), ("optional", missing_optional)]:
        for skill in skills:
            name = skill["name"]
            w = weights[tier]
            priority = w * 1.0  # (1 - match_score), match_score=0 for missing
            all_missing.append({"name": name, "tier": tier, "priority": priority, "weight": w})

    # Sort by priority (essential first), then respect prerequisites
    all_missing.sort(key=lambda x: -x["priority"])
    ordered = _topological_sort(all_missing)

    # Group into weeks (2-3 skills per week)
    roadmap = []
    skills_per_week = max(len(ordered) / total_weeks, 1) if ordered else 2
    skills_per_week = min(max(skills_per_week, 1.5), 3)

    week = 1
    idx = 0
    while idx < len(ordered) and week <= total_weeks:
        week_skills = []
        count = 0
        while idx < len(ordered) and count < int(skills_per_week + 0.5):
            skill = ordered[idx]
            difficulty = SKILL_DIFFICULTY.get(skill["name"], "intermediate")
            resources = LEARNING_RESOURCES.get(skill["name"], _make_default_resources(skill["name"]))

            hours = {"beginner": 4, "intermediate": 6, "advanced": 10}.get(difficulty, 6)

            week_skills.append({
                "week_number": week,
                "skill_name": skill["name"],
                "tier": skill["tier"],
                "difficulty": difficulty,
                "estimated_hours": hours,
                "resources": resources,
                "tasks": {
                    "practice": resources.get("practice", "Complete exercises"),
                    "project": resources.get("project", "Build a mini-project")
                },
                "project_idea": resources.get("project", "Build a project using this skill"),
                "is_completed": False
            })
            idx += 1
            count += 1

        roadmap.extend(week_skills)
        week += 1

    return roadmap


def _topological_sort(skills):
    """Sort skills respecting prerequisites."""
    skill_names = {s["name"] for s in skills}
    skill_map = {s["name"]: s for s in skills}

    visited = set()
    result = []

    def visit(name):
        if name in visited or name not in skill_map:
            return
        visited.add(name)
        prereqs = SKILL_PREREQUISITES.get(name, [])
        for p in prereqs:
            if p in skill_map:
                visit(p)
        result.append(skill_map[name])

    # Visit essential first, then recommended, then optional
    for tier in ["essential", "recommended", "optional"]:
        for s in skills:
            if s["tier"] == tier:
                visit(s["name"])

    return result


def _make_default_resources(skill_name):
    return {
        "courses": [f"https://www.coursera.org/search?query={skill_name.replace(' ', '+')}"],
        "youtube": [f"https://www.youtube.com/results?search_query={skill_name.replace(' ', '+')}+tutorial"],
        "docs": [f"https://www.google.com/search?q={skill_name.replace(' ', '+')}+documentation"],
        "practice": f"Complete online tutorials and exercises for {skill_name}",
        "project": f"Build a small project demonstrating {skill_name}"
    }
