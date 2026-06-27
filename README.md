# CIRS — Candidate Intelligent Ranking System
### India Runs Data & AI Challenge | Redrob Hackathon

> Rank candidates the way a great recruiter would — using semantic understanding, not just keyword matching.

---

## Solution Overview

CIRS is a **hybrid AI ranking engine** that evaluates candidates across six rule-based dimensions and blends them with **semantic profile matching** (vector similarity between full JD and candidate profiles).

| Layer | Approach |
|---|---|
| **Semantic Search** | TF-IDF vector embeddings (default) or sentence-transformers |
| **Rule-Based Scoring** | 6 weighted dimensions with synonym-aware skill matching |
| **Hybrid Model** | 65% rule-based + 35% semantic profile similarity |
| **Behavioral Signals** | Projects, certifications, platform activity, open-source engagement |

### Scoring Dimensions

| Dimension | Weight | What It Captures |
|---|---|---|
| Skill Match | 30% | Exact/synonym + semantic skill overlap |
| Experience | 22% | YOE alignment, company prestige, career progression |
| Platform Signals | 18% | GitHub stars, contributions, PRs + LinkedIn activity |
| Education | 10% | College tier, CGPA, certifications |
| Practical Fit | 10% | CTC range, notice period, location |
| Behavioral | 10% | Projects, certs, engagement signals |

---

## Quick Start

```bash
cd candidate-ranking
pip install -r requirements.txt
python main.py
```

### Outputs

| File | Description |
|---|---|
| `output/ranked_candidates.csv` | Full ranked list (all candidates) |
| `output/shortlist_top50.csv` | Recruiter-ready top-50 shortlist |
| `output/ranking_summary.json` | Score stats + top 10 + methodology |
| `output/CIRS_Approach_Deck.pdf` | Architecture & methodology deck |

---

## Project Structure

```
candidate-ranking/
├── main.py                      # CLI entry point
├── requirements.txt
├── README.md
├── src/
│   ├── cirs/                    # Core ranking package
│   │   ├── config.py            # Weights & tier mappings
│   │   ├── profiles.py          # JD/candidate text builders
│   │   ├── semantic.py          # TF-IDF / transformer embeddings
│   │   ├── scorers.py           # Dimension scorers
│   │   ├── hybrid_ranker.py     # Hybrid ranking engine
│   │   └── pipeline.py          # End-to-end orchestration
│   ├── generate_dataset.py      # Synthetic data generator
│   ├── generate_pdf.py          # Approach deck generator
│   └── ranking_engine.py        # Backward-compatible wrapper
├── data/
│   ├── candidates.json
│   ├── candidates.csv
│   └── job_description.json
├── output/
│   └── ...
└── tests/
    └── test_ranking.py
```

---

## Architecture

```
Job Description (JSON)          Candidate Profiles (JSON)
         │                                │
         └──────────┬─────────────────────┘
                    ▼
         ┌──────────────────────┐
         │  Profile Text Builder │
         └──────────┬───────────┘
                    ▼
    ┌───────────────────────────────────┐
    │     Semantic Engine (TF-IDF/ST)    │──► semantic_profile_score
    └───────────────────────────────────┘
                    │
    ┌───────────────┴───────────────────┐
    │  6 Rule-Based Dimension Scorers   │──► rule_based_score
    └───────────────┬───────────────────┘
                    ▼
         ┌──────────────────────┐
         │   Hybrid Blender     │
         │  65% rule + 35% sem  │──► composite_score (0–100)
         └──────────┬───────────┘
                    ▼
           Ranked CSV + Shortlist
```

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Optional: Deep Semantic Search

For production-grade embeddings, install sentence-transformers:

```bash
pip install sentence-transformers
```

The engine auto-detects and uses `all-MiniLM-L6-v2` when available.

---

## Extending

- **LLM ranking**: Add `OPENAI_API_KEY` and plug an LLM re-ranker on top-50
- **Fine-tune weights**: Edit `src/cirs/config.py` → `ScoringConfig`
- **Real datasets**: Replace `data/candidates.json` and `data/job_description.json`

---

## License

MIT
