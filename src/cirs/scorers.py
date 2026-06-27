"""Rule-based dimension scorers for candidate evaluation."""

from __future__ import annotations

import math
import re

import numpy as np

from cirs.config import COLLEGE_TIER_SCORES, COMPANY_PRESTIGE_MAP, SKILL_SYNONYMS, ScoringConfig
from cirs.profiles import build_skills_text
from cirs.semantic import SemanticEngine


def normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    for canonical, variants in SKILL_SYNONYMS.items():
        if s in variants:
            return canonical
    return s


def split_skill_options(skill: str) -> list[str]:
    skill_text = skill.lower().strip()
    skill_text = skill_text.replace("/", " or ")
    skill_text = skill_text.replace(",", " or ")
    options = [opt.strip() for opt in re.split(r"\s+or\s+", skill_text) if opt.strip()]
    return [normalize_skill(option) for option in options]


def exact_skill_match_score(
    candidate_skills: list[str], jd_required: list[str], jd_nice: list[str]
) -> dict:
    cand_norm = {normalize_skill(s) for s in candidate_skills}
    req_norm_options = [split_skill_options(s) for s in jd_required]
    nice_norm_options = [split_skill_options(s) for s in jd_nice]

    req_hits = sum(1 for options in req_norm_options if any(opt in cand_norm for opt in options))
    nice_hits = sum(1 for options in nice_norm_options if any(opt in cand_norm for opt in options))

    req_coverage = req_hits / max(len(req_norm_options), 1)
    nice_coverage = nice_hits / max(len(nice_norm_options), 1)
    raw = (req_coverage * 0.70) + (nice_coverage * 0.30)
    score = round(raw * 100, 2)

    matched_skills = []
    for options in req_norm_options:
        for opt in options:
            if opt in cand_norm:
                matched_skills.append(opt)
                break

    return {
        "score": score,
        "required_matched": req_hits,
        "required_total": len(req_norm_options),
        "nice_matched": nice_hits,
        "nice_total": len(nice_norm_options),
        "matched_skills": matched_skills,
    }


def hybrid_skill_match_score(
    candidate_skills: list[str],
    jd_required: list[str],
    jd_nice: list[str],
    semantic_engine: SemanticEngine,
    config: ScoringConfig,
) -> dict:
    exact = exact_skill_match_score(candidate_skills, jd_required, jd_nice)
    jd_skill_text = build_skills_text(jd_required + jd_nice)
    cand_skill_text = build_skills_text(candidate_skills)
    semantic = semantic_engine.score_skill_overlap(jd_skill_text, cand_skill_text)

    blended = (
        exact["score"] * config.skill_exact_blend
        + semantic * config.skill_semantic_blend
    )
    return {
        **exact,
        "score": round(blended, 2),
        "semantic_skill_score": semantic,
    }


def experience_score(candidate: dict, jd: dict) -> dict:
    yoe = candidate.get("years_of_experience", 0)

    exp_str = jd.get("experience_required", "3-7 years")
    numbers = [int(x) for x in re.findall(r"\d+", exp_str)]
    min_exp = numbers[0] if numbers else 2
    max_exp = numbers[1] if len(numbers) > 1 else min_exp + 4

    if min_exp <= yoe <= max_exp:
        yoe_score = 100
    elif yoe < min_exp:
        yoe_score = max(0, 100 - (min_exp - yoe) * 20)
    else:
        yoe_score = max(60, 100 - (yoe - max_exp) * 5)

    history = candidate.get("work_history", [])
    if history:
        prestige_scores = [
            COMPANY_PRESTIGE_MAP.get(c.get("type", "startup"), 40) for c in history
        ]
        weights = [1.5 if i == 0 else 1.0 for i in range(len(prestige_scores))]
        prestige_score = float(np.average(prestige_scores, weights=weights[: len(prestige_scores)]))
    else:
        prestige_score = 20.0

    if history:
        tenures = [c.get("tenure_years", 1) for c in history]
        progression_score = min(100, float(np.mean(tenures)) * 30)
    else:
        progression_score = 50.0

    final = (yoe_score * 0.50) + (prestige_score * 0.35) + (progression_score * 0.15)
    return {
        "score": round(final, 2),
        "yoe": yoe,
        "yoe_score": round(yoe_score, 1),
        "prestige": round(prestige_score, 1),
        "progression": round(progression_score, 1),
    }


def platform_signal_score(candidate: dict) -> dict:
    gh = candidate.get("github", {})
    li = candidate.get("linkedin", {})

    if not gh.get("active", False):
        gh_score = 10.0
    else:
        stars = gh.get("total_stars", 0)
        star_score = min(100, math.log1p(stars) / math.log1p(2000) * 100)
        contribs = gh.get("contributions_last_year", 0)
        contrib_score = min(100, contribs / 1500 * 100)
        prs = gh.get("merged_prs", 0)
        pr_score = min(100, prs / 200 * 100)
        repos = gh.get("public_repos", 0)
        repo_score = min(100, repos / 50 * 100)
        gh_score = star_score * 0.35 + contrib_score * 0.35 + pr_score * 0.20 + repo_score * 0.10

    conns = li.get("connections", 0)
    conn_score = min(100, conns / 2000 * 100)
    recs = li.get("recommendations", 0)
    rec_score = min(100, recs / 20 * 100)
    posts = li.get("posts_last_6m", 0)
    post_score = min(100, posts / 100 * 100)
    endorse = li.get("endorsements", 0)
    endorse_score = min(100, endorse / 200 * 100)
    li_score = conn_score * 0.25 + rec_score * 0.40 + post_score * 0.20 + endorse_score * 0.15

    final = (gh_score * 0.60) + (li_score * 0.40)
    return {
        "score": round(final, 2),
        "github_score": round(gh_score, 1),
        "linkedin_score": round(li_score, 1),
    }


def education_score(candidate: dict) -> dict:
    edu = candidate.get("education", {})
    tier = edu.get("tier", "Tier-3")
    cgpa = edu.get("cgpa", 6.0)
    certs = len(candidate.get("certifications", []))

    tier_score = COLLEGE_TIER_SCORES.get(tier, 35)
    cgpa_score = max(0, (cgpa - 5.0) / 4.8 * 100)
    cert_score = min(100, certs * 25)

    final = (tier_score * 0.50) + (cgpa_score * 0.35) + (cert_score * 0.15)
    return {"score": round(final, 2), "tier": tier, "cgpa": cgpa, "certifications": certs}


def fit_score(candidate: dict, jd: dict) -> dict:
    ctc_range = jd.get("ctc_range_lpa", [20, 50])
    max_notice = jd.get("notice_period_max_days", 60)

    cand_ctc = candidate.get("expected_ctc_lpa", 20)
    if ctc_range[0] <= cand_ctc <= ctc_range[1]:
        ctc_score = 100
    elif cand_ctc < ctc_range[0]:
        ctc_score = max(60, 100 - (ctc_range[0] - cand_ctc) * 5)
    else:
        ctc_score = max(0, 100 - (cand_ctc - ctc_range[1]) * 8)

    notice = candidate.get("notice_period_days", 30)
    notice_score = 100 if notice <= max_notice else max(0, 100 - (notice - max_notice) * 2)

    jd_location = jd.get("location", "Bangalore").lower()
    cand_location = candidate.get("location", "").lower()
    remote_ok = candidate.get("open_to_remote", False)

    if any(city in cand_location for city in ["bangalore", "bengaluru"]) and "bangalore" in jd_location:
        location_score = 100
    elif remote_ok and "hybrid" in jd_location:
        location_score = 85
    elif remote_ok:
        location_score = 75
    else:
        location_score = 50

    final = (ctc_score * 0.40) + (notice_score * 0.35) + (location_score * 0.25)
    return {"score": round(final, 2), "ctc": cand_ctc, "notice_days": notice}


def behavioral_score(candidate: dict, jd: dict) -> dict:
    """
    Behavioral / motivation signals from projects, certifications, and platform activity.
    Captures engagement beyond raw skills.
    """
    projects = len(candidate.get("projects", []))
    certs = len(candidate.get("certifications", []))
    gh = candidate.get("github", {})
    li = candidate.get("linkedin", {})

    project_score = min(100, projects * 25)
    cert_score = min(100, certs * 20)
    activity_score = 0.0
    if gh.get("active"):
        activity_score += min(50, gh.get("contributions_last_year", 0) / 30)
    activity_score += min(50, li.get("posts_last_6m", 0))

    preferred = " ".join(jd.get("preferred_background", [])).lower()
    bonus = 0.0
    if "open-source" in preferred or "open source" in preferred:
        if gh.get("merged_prs", 0) > 20:
            bonus += 15
    if "blog" in preferred or "papers" in preferred:
        if li.get("posts_last_6m", 0) > 30:
            bonus += 10

    raw = project_score * 0.35 + cert_score * 0.25 + activity_score * 0.40 + bonus
    return {"score": round(min(100, raw), 2), "projects": projects, "certifications": certs}
