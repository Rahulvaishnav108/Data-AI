from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


def _parse_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    # Accept comma, semicolon, and pipe-delimited lists.
    parts = [part.strip() for part in re.split(r"[;,|]", text) if part.strip()]
    return parts


def _parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def _parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "yes", "y", "1"}:
        return True
    if text in {"false", "no", "n", "0"}:
        return False
    return default


def _get_first(row: dict[str, str], keys: list[str], default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def load_candidates(data_dir: Path | str = "data") -> list[dict]:
    data_path = Path(data_dir)
    json_path = data_path / "candidates.json"
    csv_path = data_path / "candidates.csv"

    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if not csv_path.exists():
        raise FileNotFoundError(
            "No candidate dataset found. Please provide data/candidates.json or data/candidates.csv"
        )

    rows = _read_csv(csv_path)
    candidates: list[dict] = []
    for row in rows:
        location = str(row.get("location", "")).strip()
        open_to_remote = _parse_bool(row.get("open_to_remote"), default=(location.lower() == "remote"))

        github_stars = _parse_int(_get_first(row, ["github_stars", "stars", "total_stars"]))
        github_contributions = _parse_int(_get_first(row, ["github_contributions", "contributions_last_year"]))
        github_prs = _parse_int(_get_first(row, ["github_prs", "merged_prs"]))
        linkedin_posts = _parse_int(_get_first(row, ["linkedin_posts", "posts_last_6m", "posts"]))
        expected_ctc = _parse_float(_get_first(row, ["expected_ctc_lpa", "expected_ctc", "ctc"]))

        candidates.append(
            {
                "candidate_id": str(row.get("candidate_id", "")).strip(),
                "name": str(row.get("name", "")).strip() or str(row.get("candidate_id", "")).strip(),
                "years_of_experience": _parse_int(row.get("years_experience")),
                "career_stage": str(row.get("career_stage", "")).strip(),
                "education": {
                    "college": str(row.get("college", "")).strip(),
                    "tier": str(row.get("college_tier", "")).strip(),
                    "cgpa": _parse_float(_get_first(row, ["cgpa", "grade", "score"]), 0.0),
                    "degree": str(row.get("degree", "")).strip(),
                    "field": str(row.get("field", "")).strip(),
                },
                "skills": _parse_list(_get_first(row, ["skills", "skill_set"])),
                "work_history": [],
                "certifications": _parse_list(_get_first(row, ["certifications", "certs"])),
                "projects": _parse_list(_get_first(row, ["projects", "project_list"])),
                "github": {
                    "active": github_stars > 0 or github_contributions > 0 or github_prs > 0,
                    "public_repos": _parse_int(_get_first(row, ["public_repos", "repos"])),
                    "total_stars": github_stars,
                    "contributions_last_year": github_contributions,
                    "merged_prs": github_prs,
                },
                "linkedin": {
                    "connections": _parse_int(_get_first(row, ["linkedin_connections", "connections"])),
                    "recommendations": _parse_int(_get_first(row, ["linkedin_recommendations", "recommendations"])),
                    "posts_last_6m": linkedin_posts,
                    "endorsements": _parse_int(_get_first(row, ["linkedin_endorsements", "endorsements"])),
                },
                "location": location,
                "open_to_remote": open_to_remote,
                "notice_period_days": _parse_int(row.get("notice_period_days"), default=0),
                "expected_ctc_lpa": expected_ctc,
            }
        )
    return candidates


def load_job_description(data_dir: Path | str = "data") -> dict:
    data_path = Path(data_dir)
    json_path = data_path / "job_description.json"
    csv_path = data_path / "job_description.csv"

    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if not csv_path.exists():
        raise FileNotFoundError(
            "No job description file found. Please provide data/job_description.json or data/job_description.csv"
        )

    rows = _read_csv(csv_path)
    if not rows:
        raise ValueError("job_description.csv is empty")

    row = rows[0]
    return {
        "job_id": str(row.get("job_id", "")).strip(),
        "title": str(row.get("title", "")).strip(),
        "company": str(row.get("company", "")).strip(),
        "location": str(row.get("location", "")).strip(),
        "experience_required": str(row.get("experience_required", "")).strip(),
        "required_skills": _parse_list(_get_first(row, ["required_skills", "required_skill_set"])),
        "good_to_have": _parse_list(_get_first(row, ["good_to_have", "nice_to_have", "preferred_skills"])),
        "responsibilities": _parse_list(_get_first(row, ["responsibilities", "responsibility_list"])),
        "preferred_background": _parse_list(_get_first(row, ["preferred_background", "preferred_backgrounds"])),
        "education": str(row.get("education", "")).strip(),
        "ctc_range_lpa": [
            _parse_float(_get_first(row, ["ctc_min", "ctc_range_min", "ctc_range_lpa_min"]), 0.0),
            _parse_float(_get_first(row, ["ctc_max", "ctc_range_max", "ctc_range_lpa_max"]), 0.0),
        ],
        "notice_period_max_days": _parse_int(_get_first(row, ["notice_period_max_days", "max_notice_period", "notice_period_max"]), 0),
    }
