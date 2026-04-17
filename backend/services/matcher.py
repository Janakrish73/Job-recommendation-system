from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import numpy as np


class JobMatcher:
    """
    Core recommendation engine.

    Uses two approaches:
    1. Set-based matching → exact skill count match percentage
    2. TF-IDF cosine similarity → weighted semantic matching

    Final score = weighted average of both.
    """

    def compute_match(
        self,
        user_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Compute match between user skills and job required skills.

        Returns:
            score         - float 0-100 (match percentage)
            matched_skills - skills the user already has
            missing_skills - skills the user needs
        """
        if not job_skills:
            return {"score": 0.0, "matched_skills": [], "missing_skills": []}

        user_set = {s.lower().strip() for s in user_skills}
        job_set = {s.lower().strip() for s in job_skills}

        matched = user_set & job_set
        missing = job_set - user_set

        # ── Method 1: Set-based score ──────────────────────────────────────
        set_score = len(matched) / len(job_set) * 100

        # ── Method 2: TF-IDF cosine similarity ────────────────────────────
        tfidf_score = self._tfidf_score(list(user_set), list(job_set))

        # ── Final: weighted average (60% set-based, 40% TF-IDF) ───────────
        final_score = round(0.6 * set_score + 0.4 * tfidf_score, 1)
        final_score = min(100.0, max(0.0, final_score))

        return {
            "score": final_score,
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing)),
        }

    def _tfidf_score(self, user_skills: List[str], job_skills: List[str]) -> float:
        """TF-IDF cosine similarity between user and job skill texts."""
        if not user_skills or not job_skills:
            return 0.0
        try:
            user_text = " ".join(user_skills)
            job_text = " ".join(job_skills)
            vec = TfidfVectorizer(ngram_range=(1, 2))
            matrix = vec.fit_transform([user_text, job_text])
            score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
            return float(score) * 100
        except Exception:
            return 0.0

    def rank_jobs(
        self,
        user_skills: List[str],
        all_jobs: List[Dict[str, Any]],
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Rank jobs by match score (descending).

        all_jobs format:
        [
            {
                "job_id": 1,
                "title": "Python Developer",
                "company": "Acme Corp",
                "location": "Remote",
                "job_type": "full_time",
                "salary_min": 50000,
                "salary_max": 80000,
                "description": "...",
                "required_skills": ["Python", "SQL", "Docker"]
            },
            ...
        ]
        """
        results = []
        for job in all_jobs:
            required = job.get("required_skills", [])
            match = self.compute_match(user_skills, required)

            if match["score"] >= min_score:
                results.append({
                    "job_id": job["job_id"],
                    "title": job["title"],
                    "company": job["company"],
                    "location": job.get("location"),
                    "job_type": job.get("job_type", "full_time"),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "description": job.get("description"),
                    "match_score": match["score"],
                    "matched_skills": match["matched_skills"],
                    "missing_skills": match["missing_skills"],
                    "required_skills": required,
                })

        # Sort by score descending
        return sorted(results, key=lambda x: x["match_score"], reverse=True)


# ── Optional: Sentence Transformer Matcher (upgrade path) ────────────────────

class SemanticJobMatcher(JobMatcher):
    """
    Enhanced matcher using Sentence Transformers.
    Understands synonyms: 'ML' matches 'Machine Learning'.

    Install: pip install sentence-transformers
    First run downloads ~80MB model.

    Use this in place of JobMatcher for better accuracy.
    """

    def __init__(self):
        super().__init__()
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer("all-MiniLM-L6-v2")
                print("[SemanticMatcher] Model loaded.")
            except ImportError:
                print("[SemanticMatcher] sentence-transformers not installed, falling back to TF-IDF.")
        return self._model

    def _tfidf_score(self, user_skills: List[str], job_skills: List[str]) -> float:
        model = self._load_model()
        if model is None:
            return super()._tfidf_score(user_skills, job_skills)

        user_text = ", ".join(user_skills)
        job_text = ", ".join(job_skills)
        embeddings = model.encode([user_text, job_text])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(score) * 100


# Use basic matcher by default; switch to SemanticJobMatcher for better results
matcher = JobMatcher()
