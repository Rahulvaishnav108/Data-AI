"""End-to-end CIRS pipeline orchestration."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from cirs.config import DEFAULT_CONFIG
from cirs.hybrid_ranker import rank_candidates

logger = logging.getLogger(__name__)


def run_pipeline(
    data_dir: Path | str = "data",
    output_dir: Path | str = "output",
    generate_pdf: bool = True,
) -> "pd.DataFrame":
    import pandas as pd  # noqa: F401 — returned type

    data_path = Path(data_dir)
    output_path = Path(output_dir)
    data_path.mkdir(exist_ok=True)
    output_path.mkdir(exist_ok=True)

    candidates_file = data_path / "candidates.json"
    jd_file = data_path / "job_description.json"

    print("=" * 60)
    print("  CIRS — Candidate Intelligent Ranking System v2")
    print("  India Runs Data & AI Challenge | Redrob")
    print("=" * 60)

    if not candidates_file.exists() or not jd_file.exists():
        print("\n[1/4] Generating synthetic dataset...")
        from generate_dataset import generate_all

        generate_all(str(data_path))
    else:
        print("\n[1/4] Loading existing dataset...")

    with open(candidates_file, encoding="utf-8") as f:
        candidates = json.load(f)
    with open(jd_file, encoding="utf-8") as f:
        jd = json.load(f)

    print(f"   OK  {len(candidates)} candidates | JD: {jd['title']}")

    print("\n[2/4] Running hybrid AI ranking (rule-based + semantic)...")
    ranked = rank_candidates(candidates, jd, DEFAULT_CONFIG)
    backend = ranked["ranking_method"].iloc[0] if len(ranked) else "hybrid"
    print(f"   OK  Ranking complete ({backend})")

    print("\n[3/4] Exporting results...")
    ranked.to_csv(output_path / "ranked_candidates.csv", index=False)
    ranked.head(50).to_csv(output_path / "shortlist_top50.csv", index=False)

    cfg = DEFAULT_CONFIG
    summary = {
        "total_candidates": len(candidates),
        "job_title": jd["title"],
        "ranking_approach": "hybrid (rule-based + semantic embeddings)",
        "semantic_backend": backend,
        "top_10": ranked.head(10)[
            [
                "rank",
                "candidate_id",
                "composite_score",
                "rule_based_score",
                "semantic_profile_score",
                "skill_match_score",
                "years_experience",
                "career_stage",
                "college_tier",
            ]
        ].to_dict("records"),
        "score_stats": ranked["composite_score"].describe().round(2).to_dict(),
        "weights_used": {
            "hybrid_blend": f"{cfg.rule_based_blend:.0%} rule-based + {cfg.semantic_blend:.0%} semantic",
            **{k: f"{v:.0%}" for k, v in cfg.dimension_weights().items()},
        },
    }
    with open(output_path / "ranking_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"   OK  output/ranked_candidates.csv")
    print(f"   OK  output/shortlist_top50.csv")
    print(f"   OK  output/ranking_summary.json")

    if generate_pdf:
        print("\n[4/4] Generating approach deck PDF...")
        try:
            from generate_pdf import generate_deck

            generate_deck(str(output_path / "CIRS_Approach_Deck.pdf"), ranked, jd)
            print("   OK  output/CIRS_Approach_Deck.pdf")
        except ImportError as e:
            print(f"   SKIP  PDF skipped (install reportlab): {e}")
    else:
        print("\n[4/4] PDF generation skipped")

    _print_top_10(ranked, jd["title"])
    return ranked


def _print_top_10(ranked, job_title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  TOP 10 CANDIDATES — {job_title}")
    print(f"{'=' * 70}")
    cols = [
        "rank",
        "candidate_id",
        "composite_score",
        "semantic_profile_score",
        "skill_match_score",
        "experience_score",
        "required_skills_matched",
        "career_stage",
    ]
    print(ranked.head(10)[cols].to_string(index=False))
    print(f"\n  Score Distribution:")
    print(
        f"  Avg: {ranked['composite_score'].mean():.1f} | "
        f"Top: {ranked['composite_score'].max():.1f} | "
        f"Bot: {ranked['composite_score'].min():.1f}"
    )
    print(f"{'=' * 70}")
