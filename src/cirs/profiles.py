"""Build rich text profiles for semantic matching."""

from __future__ import annotations


def build_jd_text(jd: dict) -> str:
    """Aggregate JD fields into a single document for embedding."""
    parts = [
        jd.get("title", ""),
        jd.get("company", ""),
        jd.get("location", ""),
        jd.get("experience_required", ""),
        " ".join(jd.get("required_skills", [])),
        " ".join(jd.get("good_to_have", [])),
        " ".join(jd.get("responsibilities", [])),
        " ".join(jd.get("preferred_background", [])),
        jd.get("education", ""),
    ]
    return " ".join(p.strip() for p in parts if p and str(p).strip())


def build_candidate_text(candidate: dict) -> str:
    """Aggregate candidate profile fields into a single document for embedding."""
    edu = candidate.get("education", {})
    work = candidate.get("work_history", [])
    work_text = " ".join(
        f"{w.get('role', '')} at {w.get('company', '')} ({w.get('type', '')})"
        for w in work
    )
    parts = [
        candidate.get("name", ""),
        candidate.get("career_stage", ""),
        f"{candidate.get('years_of_experience', 0)} years experience",
        " ".join(candidate.get("skills", [])),
        " ".join(candidate.get("projects", [])),
        " ".join(candidate.get("certifications", [])),
        edu.get("degree", ""),
        edu.get("field", ""),
        edu.get("college", ""),
        edu.get("tier", ""),
        work_text,
        candidate.get("location", ""),
    ]
    return " ".join(p.strip() for p in parts if p and str(p).strip())


def build_skills_text(skills: list[str]) -> str:
    return " ".join(skills)
