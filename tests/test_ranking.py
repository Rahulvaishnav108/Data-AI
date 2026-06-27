"""Tests for CIRS hybrid ranking engine."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cirs.data_loader import load_candidates, load_job_description  # noqa: E402
from cirs.hybrid_ranker import rank_candidates  # noqa: E402
from cirs.scorers import normalize_skill, exact_skill_match_score  # noqa: E402
from cirs.semantic import SemanticEngine  # noqa: E402


@pytest.fixture
def sample_jd():
    return {
        "title": "Senior ML Engineer",
        "experience_required": "3-7 years",
        "required_skills": ["Python", "Machine Learning", "NLP", "SQL"],
        "good_to_have": ["LLMs", "Docker"],
        "responsibilities": ["Build NLP pipelines"],
        "preferred_background": ["open-source contributions"],
        "ctc_range_lpa": [20, 50],
        "notice_period_max_days": 60,
        "location": "Bangalore (Hybrid)",
    }


@pytest.fixture
def sample_candidates():
    return [
        {
            "candidate_id": "CAND_0001",
            "name": "Alice",
            "years_of_experience": 5,
            "career_stage": "mid",
            "skills": ["Python", "ML", "NLP", "SQL", "Docker"],
            "work_history": [{"company": "Flipkart", "type": "unicorn", "tenure_years": 3, "role": "ML Engineer"}],
            "education": {"tier": "IIT", "cgpa": 8.5},
            "certifications": ["AWS ML"],
            "projects": ["RAG Chatbot"],
            "github": {"active": True, "total_stars": 500, "contributions_last_year": 800, "merged_prs": 40, "public_repos": 20},
            "linkedin": {"connections": 1500, "recommendations": 10, "posts_last_6m": 50, "endorsements": 100},
            "location": "Bangalore",
            "open_to_remote": True,
            "notice_period_days": 30,
            "expected_ctc_lpa": 35,
        },
        {
            "candidate_id": "CAND_0002",
            "name": "Bob",
            "years_of_experience": 1,
            "career_stage": "junior",
            "skills": ["Java", "Spring"],
            "work_history": [],
            "education": {"tier": "Tier-3", "cgpa": 6.0},
            "certifications": [],
            "projects": [],
            "github": {"active": False},
            "linkedin": {"connections": 100, "recommendations": 0, "posts_last_6m": 0, "endorsements": 5},
            "location": "Chennai",
            "open_to_remote": False,
            "notice_period_days": 90,
            "expected_ctc_lpa": 8,
        },
    ]


def test_skill_synonym_normalization():
    assert normalize_skill("PyTorch") == "pytorch"
    assert normalize_skill("machine learning") == "ml"


def test_exact_skill_match():
    result = exact_skill_match_score(
        ["Python", "PyTorch", "NLP"],
        ["Python", "Machine Learning", "NLP"],
        ["Docker"],
    )
    assert result["required_matched"] >= 2
    assert 0 <= result["score"] <= 100


def test_semantic_engine_returns_scores():
    engine = SemanticEngine()
    scores = engine.score_profiles(
        "Python machine learning NLP senior engineer",
        ["Python ML NLP Docker", "Java backend developer"],
    )
    assert len(scores) == 2
    assert all(0 <= s <= 100 for s in scores)
    assert scores[0] >= scores[1]


def test_rank_candidates_output_shape(sample_candidates, sample_jd):
    df = rank_candidates(sample_candidates, sample_jd)
    assert len(df) == 2
    assert list(df.columns)[0] == "rank"
    assert df.iloc[0]["composite_score"] >= df.iloc[1]["composite_score"]


def test_rank_candidates_scores_in_range(sample_candidates, sample_jd):
    df = rank_candidates(sample_candidates, sample_jd)
    for col in ["composite_score", "semantic_profile_score", "skill_match_score", "rule_based_score"]:
        assert df[col].between(0, 100).all()


def test_loader_supports_csv(tmp_path, sample_jd):
    csv_content = (
        "candidate_id,years_experience,career_stage,college_tier,cgpa,skills,certifications,github_stars,github_contributions,github_prs,linkedin_connections,linkedin_recommendations,posts_last_6m,notice_period_days,expected_ctc_lpa,location\n"
        "CAND_9999,5,mid,IIT,8.9,Python;ML;NLP,1,120,300,10,400,5,20,30,35.0,Bangalore\n"
    )
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "candidates.csv").write_text(csv_content, encoding="utf-8")
    (data_dir / "job_description.json").write_text(json.dumps(sample_jd), encoding="utf-8")

    candidates = load_candidates(data_dir)
    assert isinstance(candidates, list)
    assert candidates[0]["candidate_id"] == "CAND_9999"
    assert 0 <= candidates[0]["years_of_experience"] <= 10

    df = rank_candidates(candidates, sample_jd)
    assert df.iloc[0]["candidate_id"] == "CAND_9999"


def test_integration_with_real_data():
    data_dir = ROOT / "data"
    if not (data_dir / "candidates.json").exists():
        pytest.skip("Dataset not present")

    with open(data_dir / "candidates.json", encoding="utf-8") as f:
        candidates = json.load(f)
    with open(data_dir / "job_description.json", encoding="utf-8") as f:
        jd = json.load(f)

    df = rank_candidates(candidates[:50], jd)
    assert len(df) == 50
    assert df["rank"].tolist() == list(range(1, 51))
