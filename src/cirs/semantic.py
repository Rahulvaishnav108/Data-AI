"""Semantic similarity engine — TF-IDF vectors with optional transformer embeddings."""

from __future__ import annotations

import logging
from typing import Literal

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

Backend = Literal["sentence-transformer", "tfidf"]


class SemanticEngine:
    """
    Computes cosine similarity between job description and candidate profiles.

    Uses sentence-transformers when available; falls back to TF-IDF (no GPU/model download).
    """

    def __init__(self) -> None:
        self._backend: Backend = "tfidf"
        self._transformer = None
        self._try_load_transformer()

    @property
    def backend(self) -> Backend:
        return self._backend

    def _try_load_transformer(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer

            self._transformer = SentenceTransformer("all-MiniLM-L6-v2")
            self._backend = "sentence-transformer"
            logger.info("Semantic engine: sentence-transformers (all-MiniLM-L6-v2)")
        except ImportError:
            logger.info("Semantic engine: TF-IDF fallback (install sentence-transformers for deeper semantics)")

    def score_profiles(self, jd_text: str, candidate_texts: list[str]) -> list[float]:
        """Return 0–100 semantic fit scores for each candidate vs the JD."""
        if not candidate_texts:
            return []

        if self._backend == "sentence-transformer" and self._transformer is not None:
            return self._score_transformer(jd_text, candidate_texts)
        return self._score_tfidf(jd_text, candidate_texts)

    def score_skill_overlap(self, jd_skills_text: str, candidate_skills_text: str) -> float:
        """Semantic overlap between JD skills and candidate skills (0–100)."""
        scores = self.score_profiles(jd_skills_text, [candidate_skills_text])
        return scores[0] if scores else 0.0

    def _score_transformer(self, jd_text: str, candidate_texts: list[str]) -> list[float]:
        assert self._transformer is not None
        jd_emb = self._transformer.encode([jd_text], normalize_embeddings=True)
        cand_emb = self._transformer.encode(candidate_texts, normalize_embeddings=True)
        sims = cosine_similarity(jd_emb, cand_emb)[0]
        return [_to_percent(s) for s in sims]

    def _score_tfidf(self, jd_text: str, candidate_texts: list[str]) -> list[float]:
        corpus = [jd_text] + candidate_texts
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=8000,
            sublinear_tf=True,
        )
        matrix = vectorizer.fit_transform(corpus)
        jd_vec = matrix[0:1]
        cand_vecs = matrix[1:]
        sims = cosine_similarity(jd_vec, cand_vecs)[0]
        return [_to_percent(s) for s in sims]


def _to_percent(similarity: float) -> float:
    """Map cosine similarity [-1, 1] to a 0–100 score."""
    return round(max(0.0, min(100.0, (similarity + 1) / 2 * 100)), 2)
