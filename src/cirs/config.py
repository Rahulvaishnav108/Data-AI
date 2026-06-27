"""Central configuration for scoring weights and tier mappings."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoringConfig:
    """Tunable weights for the hybrid ranking model."""

    # Rule-based dimension weights (must sum to 1.0)
    skill_match: float = 0.30
    experience: float = 0.22
    platform_signals: float = 0.18
    education: float = 0.10
    fit: float = 0.10
    behavioral: float = 0.10

    # Top-level hybrid blend: rule-based vs semantic profile match
    rule_based_blend: float = 0.65
    semantic_blend: float = 0.35

    # Skill sub-scorer: exact/synonym vs semantic skill overlap
    skill_exact_blend: float = 0.65
    skill_semantic_blend: float = 0.35

    def dimension_weights(self) -> dict[str, float]:
        return {
            "skill_match": self.skill_match,
            "experience": self.experience,
            "platform_signals": self.platform_signals,
            "education": self.education,
            "fit": self.fit,
            "behavioral": self.behavioral,
        }


COLLEGE_TIER_SCORES = {"IIT": 100, "BITS": 85, "NIT": 75, "Tier-2": 55, "Tier-3": 35}
COMPANY_PRESTIGE_MAP = {"FAANG": 100, "unicorn": 80, "growth": 65, "startup": 45, "enterprise": 40}

SKILL_SYNONYMS: dict[str, list[str]] = {
    "ml": ["machine learning", "ml"],
    "nlp": ["nlp", "natural language processing", "text processing"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "tf", "keras"],
    "python": ["python", "py"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "llms": ["llm", "llms", "large language model", "gpt", "claude", "gemini"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented"],
    "docker": ["docker", "containerization", "containers"],
    "kubernetes": ["k8s", "kubernetes", "kubectl"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "gcp": ["gcp", "google cloud", "bigquery"],
    "fastapi": ["fastapi", "fast api"],
    "langchain": ["langchain", "lang chain"],
    "rest api": ["rest api", "rest", "api"],
    "git": ["git", "github", "version control"],
}

DEFAULT_CONFIG = ScoringConfig()
