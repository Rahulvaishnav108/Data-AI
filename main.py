"""
CIRS — Candidate Intelligent Ranking System
India Runs Data & AI Challenge | Redrob

Entry point for the hybrid ranking pipeline.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from cirs.pipeline import run_pipeline  # noqa: E402


def main() -> None:
    import os
    os.chdir(ROOT)
    run_pipeline(data_dir="data", output_dir="output", generate_pdf=True)


if __name__ == "__main__":
    main()
