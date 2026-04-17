import re
from typing import List, Set

# ─────────────────────────────────────────────────────────────────────────────
# Master Skill Dictionary
# Add more skills here as needed. All lowercase.
# ─────────────────────────────────────────────────────────────────────────────
SKILL_KEYWORDS: Set[str] = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang",
    "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "matlab",
    "perl", "bash", "shell", "powershell",

    # Web Frontend
    "react", "angular", "vue", "vuejs", "html", "css", "html5", "css3",
    "bootstrap", "tailwind", "tailwindcss", "sass", "scss", "jquery",
    "next.js", "nextjs", "gatsby", "svelte", "webpack", "vite",

    # Web Backend
    "fastapi", "django", "flask", "express", "node.js", "nodejs",
    "spring", "spring boot", "laravel", "rails", "asp.net",
    "graphql", "rest api", "restful api", "websocket",

    # Databases
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis",
    "sqlite", "oracle", "sql server", "cassandra", "dynamodb",
    "elasticsearch", "firebase", "supabase",

    # Cloud & DevOps
    "docker", "kubernetes", "k8s", "aws", "azure", "gcp",
    "google cloud", "linux", "git", "github", "gitlab", "ci/cd",
    "jenkins", "terraform", "ansible", "nginx", "apache",
    "heroku", "vercel", "netlify", "railway",

    # Machine Learning & Data Science
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "sklearn", "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "data analysis", "data science", "data engineering",
    "power bi", "tableau", "excel", "statistics", "probability",
    "neural networks", "transformers", "bert", "llm",

    # Mobile
    "android", "ios", "react native", "flutter", "dart", "xcode",

    # Architecture & Practices
    "microservices", "api design", "system design", "agile", "scrum",
    "test driven development", "tdd", "unit testing", "object oriented",
    "oop", "functional programming", "design patterns", "solid",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "project management", "time management",
}

# Multi-word skills (check these first to avoid partial matches)
MULTI_WORD_SKILLS = sorted(
    [s for s in SKILL_KEYWORDS if " " in s],
    key=len, reverse=True  # longest first
)

SINGLE_WORD_SKILLS = {s for s in SKILL_KEYWORDS if " " not in s}


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract skills from resume text using keyword matching.
    Returns a sorted list of unique skill names.
    """
    if not text:
        return []

    text_lower = text.lower()
    found: Set[str] = set()

    # Step 1: Multi-word skills (check these first)
    for skill in MULTI_WORD_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)

    # Step 2: Single-word skills
    for skill in SINGLE_WORD_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)

    # Step 3: Try spaCy for additional entity-based extraction (optional)
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:50000])
        for ent in doc.ents:
            ent_lower = ent.text.lower().strip()
            if ent_lower in SKILL_KEYWORDS:
                found.add(ent_lower)
    except Exception:
        pass  # spaCy not installed or model not downloaded — graceful degradation

    # Capitalize properly for display
    result = []
    for skill in sorted(found):
        display = _capitalize_skill(skill)
        result.append(display)

    return result


def _capitalize_skill(skill: str) -> str:
    """Properly capitalize skill names for display."""
    special_cases = {
        "css": "CSS", "html": "HTML", "html5": "HTML5", "css3": "CSS3",
        "sql": "SQL", "mysql": "MySQL", "php": "PHP", "nlp": "NLP",
        "aws": "AWS", "gcp": "GCP", "ci/cd": "CI/CD", "tdd": "TDD",
        "api": "API", "rest api": "REST API", "restful api": "RESTful API",
        "oop": "OOP", "llm": "LLM", "solid": "SOLID",
        "node.js": "Node.js", "next.js": "Next.js", "vue": "Vue",
        "react": "React", "python": "Python", "java": "Java",
        "javascript": "JavaScript", "typescript": "TypeScript",
        "tensorflow": "TensorFlow", "pytorch": "PyTorch",
        "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
        "fastapi": "FastAPI", "django": "Django", "flask": "Flask",
        "docker": "Docker", "kubernetes": "Kubernetes", "k8s": "Kubernetes",
        "linux": "Linux", "git": "Git", "github": "GitHub", "gitlab": "GitLab",
        "mongodb": "MongoDB", "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
        "redis": "Redis", "firebase": "Firebase", "supabase": "Supabase",
        "power bi": "Power BI", "tableau": "Tableau",
        "golang": "Go", "rust": "Rust", "swift": "Swift", "kotlin": "Kotlin",
    }
    return special_cases.get(skill.lower(), skill.title())


def get_all_skills_list() -> List[str]:
    """Return the full list of known skills for display/autocomplete."""
    return sorted([_capitalize_skill(s) for s in SKILL_KEYWORDS])
