"""Hybrid ranking engine — rule-based dimensions + semantic profile matching."""

from __future__ import annotations

import pandas as pd

from cirs.config import DEFAULT_CONFIG, ScoringConfig
from cirs.profiles import build_candidate_text, build_jd_text
from cirs.scorers import (
    behavioral_score,
    education_score,
    experience_score,
    fit_score,
    hybrid_skill_match_score,
    platform_signal_score,
)
from cirs.semantic import SemanticEngine


def rank_candidates(
    candidates: list[dict],
    jd: dict,
    config: ScoringConfig | None = None,
) -> pd.DataFrame:
    """
    Rank candidates using a hybrid model:
      1. Six rule-based dimension scores (including behavioral signals)
      2. Full-profile semantic similarity (TF-IDF or sentence-transformers)
      3. Weighted blend: 65% rule-based + 35% semantic
    """
    cfg = config or DEFAULT_CONFIG
    weights = cfg.dimension_weights()
    semantic_engine = SemanticEngine()

    req_skills = jd.get("required_skills", [])
    nice_skills = jd.get("good_to_have", [])

    jd_text = build_jd_text(jd)
    candidate_texts = [build_candidate_text(c) for c in candidates]
    semantic_scores = semantic_engine.score_profiles(jd_text, candidate_texts)

    results = []
    for c, semantic in zip(candidates, semantic_scores):
        skill = hybrid_skill_match_score(
            c.get("skills", []), req_skills, nice_skills, semantic_engine, cfg
        )
        exp = experience_score(c, jd)
        plat = platform_signal_score(c)
        edu = education_score(c)
        fit = fit_score(c, jd)
        behavior = behavioral_score(c, jd)

        rule_based = (
            skill["score"] * weights["skill_match"]
            + exp["score"] * weights["experience"]
            + plat["score"] * weights["platform_signals"]
            + edu["score"] * weights["education"]
            + fit["score"] * weights["fit"]
            + behavior["score"] * weights["behavioral"]
        )

        composite = (
            rule_based * cfg.rule_based_blend + semantic * cfg.semantic_blend
        )

        results.append(
            {
                "candidate_id": c["candidate_id"],
                "name": c.get("name", ""),
                "career_stage": c.get("career_stage", ""),
                "years_experience": c.get("years_of_experience", 0),
                "location": c.get("location", ""),
                "expected_ctc_lpa": c.get("expected_ctc_lpa", 0),
                "notice_period_days": c.get("notice_period_days", 30),
                "skill_match_score": skill["score"],
                "semantic_skill_score": skill.get("semantic_skill_score", 0),
                "required_skills_matched": f"{skill['required_matched']}/{skill['required_total']}",
                "matched_skills": ", ".join(skill["matched_skills"]),
                "experience_score": exp["score"],
                "yoe_score": exp["yoe_score"],
                "prestige_score": exp["prestige"],
                "platform_score": plat["score"],
                "github_score": plat["github_score"],
                "linkedin_score": plat["linkedin_score"],
                "education_score": edu["score"],
                "college_tier": edu["tier"],
                "cgpa": edu["cgpa"],
                "behavioral_score": behavior["score"],
                "fit_score": fit["score"],
                "semantic_profile_score": semantic,
                "rule_based_score": round(rule_based, 2),
                "composite_score": round(composite, 2),
                "ranking_method": f"hybrid ({semantic_engine.backend})",
            }
        )

    df = pd.DataFrame(results)
    df = df.sort_values("composite_score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df
