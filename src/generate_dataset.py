"""
Dataset Generator - Creates realistic synthetic candidate data
matching the India Runs Data & AI Challenge format
"""
import json
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

# ─── Data pools ───────────────────────────────────────────────────────────────
SKILLS_POOL = {
    "engineering": ["Python", "JavaScript", "TypeScript", "React", "Node.js", "Java", "Go",
                    "Rust", "C++", "SQL", "PostgreSQL", "MongoDB", "Redis", "Docker",
                    "Kubernetes", "AWS", "GCP", "Azure", "Git", "CI/CD", "GraphQL",
                    "REST API", "Microservices", "System Design", "LangChain", "FastAPI",
                    "Django", "Flask", "Spring Boot", "Terraform", "Kafka", "Spark"],
    "data": ["Python", "R", "SQL", "Pandas", "NumPy", "TensorFlow", "PyTorch",
             "Scikit-learn", "XGBoost", "Tableau", "Power BI", "Spark", "Hadoop",
             "Airflow", "dbt", "Snowflake", "BigQuery", "Statistics", "ML", "NLP",
             "Computer Vision", "LLMs", "RAG", "Vector Databases", "MLflow"],
    "product": ["Product Strategy", "Roadmapping", "A/B Testing", "User Research",
                "Figma", "JIRA", "SQL", "Analytics", "Stakeholder Management",
                "Agile", "Scrum", "OKRs", "Growth Metrics", "Wireframing"]
}

COMPANIES = [
    ("Google", "FAANG", 1000), ("Meta", "FAANG", 950), ("Amazon", "FAANG", 900),
    ("Microsoft", "FAANG", 880), ("Apple", "FAANG", 870), ("Flipkart", "unicorn", 800),
    ("Razorpay", "unicorn", 780), ("CRED", "unicorn", 760), ("Zepto", "unicorn", 720),
    ("Swiggy", "unicorn", 710), ("Meesho", "unicorn", 690), ("Postman", "growth", 650),
    ("Freshworks", "growth", 640), ("Zoho", "growth", 600), ("Infosys", "enterprise", 500),
    ("TCS", "enterprise", 480), ("Wipro", "enterprise", 460), ("Accenture", "enterprise", 440),
    ("HCL", "enterprise", 420), ("Tech Mahindra", "enterprise", 400),
    ("Startup X", "startup", 300), ("EarlyStage AI", "startup", 280),
    ("BootstrapCo", "startup", 260), ("GrowthHack Inc", "startup", 250),
    ("NanoTech", "startup", 220)
]

COLLEGES = [
    ("IIT Bombay", "IIT", 950), ("IIT Delhi", "IIT", 940), ("IIT Madras", "IIT", 930),
    ("IIT Kharagpur", "IIT", 920), ("IIT Kanpur", "IIT", 910), ("NIT Trichy", "NIT", 750),
    ("NIT Surathkal", "NIT", 740), ("NIT Warangal", "NIT", 730), ("BITS Pilani", "BITS", 820),
    ("BITS Goa", "BITS", 780), ("VIT Vellore", "Tier-2", 550), ("SRM University", "Tier-2", 520),
    ("Manipal Institute", "Tier-2", 530), ("Amity University", "Tier-3", 400),
    ("Generic State Eng College", "Tier-3", 350), ("Govt Eng College", "Tier-3", 380)
]

CERTIFICATIONS = [
    "AWS Solutions Architect", "Google Cloud Professional", "CKA (Kubernetes)",
    "TensorFlow Developer", "Deep Learning Specialization (Coursera)",
    "Meta Backend Developer", "Stanford ML (Coursera)", "MongoDB Associate Developer",
    "Hashicorp Terraform Associate", "Azure AI Engineer"
]

GITHUB_SIGNALS = {
    "high": {"repos": (30, 80), "stars": (200, 2000), "contributions": (500, 1500), "prs": (50, 200)},
    "medium": {"repos": (10, 30), "stars": (20, 200), "contributions": (100, 500), "prs": (10, 50)},
    "low": {"repos": (1, 10), "stars": (0, 20), "contributions": (10, 100), "prs": (0, 10)}
}

LINKEDIN_SIGNALS = {
    "high": {"connections": (800, 5000), "recommendations": (10, 30), "posts": (50, 200), "endorsements": (100, 500)},
    "medium": {"connections": (300, 800), "recommendations": (3, 10), "posts": (10, 50), "endorsements": (30, 100)},
    "low": {"connections": (50, 300), "recommendations": (0, 3), "posts": (0, 10), "endorsements": (5, 30)}
}

def rand_range(tup): return random.randint(*tup)

def generate_candidate(cid: int, role_hint: str = "engineering") -> dict:
    skills_pool = SKILLS_POOL.get(role_hint, SKILLS_POOL["engineering"])

    # Career tier influences quality signals
    career_tier = random.choices(
        ["senior", "mid", "junior", "fresher"],
        weights=[15, 35, 35, 15]
    )[0]

    yoe = {"senior": random.randint(5, 12), "mid": random.randint(2, 5),
           "junior": random.randint(0, 2), "fresher": 0}[career_tier]

    # Education
    college, college_tier, college_score = random.choice(COLLEGES)
    cgpa = round(random.uniform(6.0, 9.8), 2)

    # Skills selection
    num_skills = {"senior": random.randint(8, 15), "mid": random.randint(5, 10),
                  "junior": random.randint(3, 7), "fresher": random.randint(2, 5)}[career_tier]
    skills = random.sample(skills_pool, min(num_skills, len(skills_pool)))

    # Work history
    companies_worked = []
    remaining_yoe = yoe
    while remaining_yoe > 0:
        company, company_type, company_score = random.choice(COMPANIES)
        tenure = min(remaining_yoe, random.randint(1, 4))
        companies_worked.append({
            "company": company,
            "type": company_type,
            "prestige_score": company_score,
            "tenure_years": tenure,
            "role": f"{'Senior ' if tenure > 2 else ''}{role_hint.title()} Engineer"
        })
        remaining_yoe -= tenure

    # Platform signals
    gh_tier = random.choices(["high", "medium", "low"], weights=[20, 45, 35])[0]
    li_tier = random.choices(["high", "medium", "low"], weights=[25, 50, 25])[0]

    gh = GITHUB_SIGNALS[gh_tier]
    li = LINKEDIN_SIGNALS[li_tier]

    # Certifications
    certs = random.sample(CERTIFICATIONS, random.randint(0, 3))

    # Projects
    num_projects = {"senior": random.randint(3, 8), "mid": random.randint(2, 5),
                    "junior": random.randint(1, 3), "fresher": random.randint(0, 2)}[career_tier]

    project_types = ["ML Pipeline", "Web App", "API Service", "Data Dashboard",
                     "CLI Tool", "Browser Extension", "Mobile App", "Blockchain dApp",
                     "RAG Chatbot", "Recommendation Engine"]
    projects = random.sample(project_types, min(num_projects, len(project_types)))

    return {
        "candidate_id": f"CAND_{cid:04d}",
        "name": f"Candidate_{cid}",
        "years_of_experience": yoe,
        "career_stage": career_tier,
        "education": {
            "college": college,
            "tier": college_tier,
            "cgpa": cgpa,
            "degree": "B.Tech / B.E.",
            "field": "Computer Science" if role_hint == "engineering" else "Data Science"
        },
        "skills": skills,
        "work_history": companies_worked,
        "certifications": certs,
        "projects": projects,
        "github": {
            "active": random.random() > 0.2,
            "public_repos": rand_range(gh["repos"]),
            "total_stars": rand_range(gh["stars"]),
            "contributions_last_year": rand_range(gh["contributions"]),
            "merged_prs": rand_range(gh["prs"]),
            "activity_tier": gh_tier
        },
        "linkedin": {
            "connections": rand_range(li["connections"]),
            "recommendations": rand_range(li["recommendations"]),
            "posts_last_6m": rand_range(li["posts"]),
            "endorsements": rand_range(li["endorsements"]),
            "activity_tier": li_tier
        },
        "location": random.choice(["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune",
                                    "Chennai", "Kolkata", "Ahmedabad", "Remote"]),
        "open_to_remote": random.random() > 0.3,
        "notice_period_days": random.choice([0, 15, 30, 60, 90]),
        "expected_ctc_lpa": round(random.uniform(4, 60), 1)
    }

def generate_job_description() -> dict:
    return {
        "job_id": "JD_001",
        "title": "Senior Machine Learning Engineer",
        "company": "Redrob AI",
        "location": "Bangalore (Hybrid)",
        "experience_required": "3-7 years",
        "required_skills": [
            "Python", "Machine Learning", "NLP", "PyTorch or TensorFlow",
            "SQL", "REST API", "Docker", "Git"
        ],
        "good_to_have": [
            "LLMs", "RAG", "Vector Databases", "Kubernetes", "MLflow",
            "LangChain", "AWS or GCP", "FastAPI"
        ],
        "responsibilities": [
            "Design and deploy production ML models at scale",
            "Build NLP pipelines for candidate matching and ranking",
            "Collaborate with product and data teams on AI features",
            "Mentor junior engineers and conduct code reviews",
            "Optimize model performance and inference speed"
        ],
        "preferred_background": [
            "Strong open-source contributions",
            "Experience at product-led companies",
            "Published papers or technical blog posts a plus"
        ],
        "education": "B.Tech/M.Tech in CS or related field preferred",
        "ctc_range_lpa": [20, 50],
        "notice_period_max_days": 60
    }

def generate_all(data_dir: str = "data") -> tuple[list[dict], dict]:
    """Generate synthetic candidates + JD and write to data_dir."""
    import os
    os.makedirs(data_dir, exist_ok=True)

    candidates = [generate_candidate(i, data_dir) for i in range(1, 501)]
    jd = generate_job_description()

    with open(f"{data_dir}/candidates.json", "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2)
    with open(f"{data_dir}/job_description.json", "w", encoding="utf-8") as f:
        json.dump(jd, f, indent=2)

    df = pd.DataFrame([{
        "candidate_id": c["candidate_id"],
        "years_experience": c["years_of_experience"],
        "career_stage": c["career_stage"],
        "college_tier": c["education"]["tier"],
        "cgpa": c["education"]["cgpa"],
        "num_skills": len(c["skills"]),
        "skills": ", ".join(c["skills"]),
        "certifications": len(c["certifications"]),
        "github_stars": c["github"]["total_stars"],
        "github_contributions": c["github"]["contributions_last_year"],
        "github_prs": c["github"]["merged_prs"],
        "linkedin_connections": c["linkedin"]["connections"],
        "linkedin_recommendations": c["linkedin"]["recommendations"],
        "notice_period_days": c["notice_period_days"],
        "expected_ctc_lpa": c["expected_ctc_lpa"],
        "location": c["location"],
    } for c in candidates])
    df.to_csv(f"{data_dir}/candidates.csv", index=False)

    print(f"Generated {len(candidates)} candidates -> {data_dir}/")
    return candidates, jd

if __name__ == "__main__":
    print("Generating dataset...")
    candidates = [generate_candidate(i, "data") for i in range(1, 501)]
    jd = generate_job_description()

    with open("data/candidates.json", "w") as f:
        json.dump(candidates, f, indent=2)

    with open("data/job_description.json", "w") as f:
        json.dump(jd, f, indent=2)

    df = pd.DataFrame([{
        "candidate_id": c["candidate_id"],
        "years_experience": c["years_of_experience"],
        "career_stage": c["career_stage"],
        "college_tier": c["education"]["tier"],
        "cgpa": c["education"]["cgpa"],
        "num_skills": len(c["skills"]),
        "skills": ", ".join(c["skills"]),
        "certifications": len(c["certifications"]),
        "github_stars": c["github"]["total_stars"],
        "github_contributions": c["github"]["contributions_last_year"],
        "github_prs": c["github"]["merged_prs"],
        "linkedin_connections": c["linkedin"]["connections"],
        "linkedin_recommendations": c["linkedin"]["recommendations"],
        "notice_period_days": c["notice_period_days"],
        "expected_ctc_lpa": c["expected_ctc_lpa"],
        "location": c["location"]
    } for c in candidates])

    df.to_csv("data/candidates.csv", index=False)
    print(f"✅ Generated {len(candidates)} candidates → data/candidates.json & data/candidates.csv")
    print(f"✅ Job description → data/job_description.json")
