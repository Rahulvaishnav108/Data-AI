"""
Backward-compatible ranking entry point.
Delegates to the cirs hybrid ranking engine.
"""

from cirs.hybrid_ranker import rank_candidates

__all__ = ["rank_candidates"]

if __name__ == "__main__":
    import json
    from pathlib import Path

    print("Loading data...")
    with open("data/candidates.json", encoding="utf-8") as f:
        candidates = json.load(f)
    with open("data/job_description.json", encoding="utf-8") as f:
        jd = json.load(f)

    print(f"Ranking {len(candidates)} candidates for: {jd['title']}")
    ranked = rank_candidates(candidates, jd)

    output_path = Path("output/ranked_candidates.csv")
    output_path.parent.mkdir(exist_ok=True)
    ranked.to_csv(output_path, index=False)

    print(f"\nRanking complete! Output -> {output_path}")
    cols = [
        "rank", "candidate_id", "career_stage", "composite_score",
        "semantic_profile_score", "skill_match_score", "required_skills_matched",
    ]
    print(ranked.head(10)[cols].to_string(index=False))
