from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.user import User
from models.job import Job
from models.skill import SkillResource
from schemas.job import RecommendationResponse, RecommendationResult
from services.matcher import matcher
from utils.auth import get_current_user

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.get("/me", response_model=RecommendationResponse)
def get_my_recommendations(
    min_score: float = Query(0.0, ge=0, le=100, description="Minimum match score (0-100)"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get job recommendations for the currently logged-in user.
    Jobs are ranked by skill match percentage (highest first).
    """
    # Get user's skill names
    user_skills = [us.skill.name for us in current_user.user_skills]

    # Get all active jobs with their required skills
    jobs = db.query(Job).filter(Job.is_active == True).all()

    all_jobs_data = []
    for job in jobs:
        required_skills = [js.skill.name for js in job.job_skills if js.is_required]
        all_jobs_data.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "description": job.description,
            "required_skills": required_skills,
        })

    # Rank jobs
    ranked = matcher.rank_jobs(user_skills, all_jobs_data, min_score=min_score)

    # Build response
    recommendations = [
        RecommendationResult(**r) for r in ranked[:limit]
    ]

    return RecommendationResponse(
        user_id=current_user.id,
        user_name=current_user.full_name,
        user_skills=user_skills,
        total_jobs_analyzed=len(jobs),
        recommendations=recommendations
    )


@router.get("/gap/{job_id}")
def get_skill_gap_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed skill gap analysis for a specific job.
    Shows matched skills, missing skills, and learning resources.
    """
    job = db.query(Job).filter(Job.id == job_id, Job.is_active == True).first()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    user_skills = [us.skill.name for us in current_user.user_skills]
    required_skills = [js.skill.name for js in job.job_skills if js.is_required]
    optional_skills = [js.skill.name for js in job.job_skills if not js.is_required]

    match = matcher.compute_match(user_skills, required_skills)

    # Get learning resources for missing skills
    missing_with_resources = []
    for skill_name in match["missing_skills"]:
        from models.skill import Skill
        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        resources = []
        if skill:
            resources = [
                {"platform": r.platform, "url": r.url, "is_free": r.is_free}
                for r in skill.resources
            ]
        # Default resources if none in DB
        if not resources:
            resources = _default_resources(skill_name)
        missing_with_resources.append({
            "skill": skill_name,
            "resources": resources
        })

    return {
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "description": job.description,
        },
        "match_score": match["score"],
        "matched_skills": match["matched_skills"],
        "missing_required_skills": missing_with_resources,
        "optional_skills": optional_skills,
        "user_skills": user_skills,
        "required_skills": required_skills,
    }


def _default_resources(skill_name: str) -> list:
    """Return default learning resource links for a skill."""
    skill_lower = skill_name.lower().replace(" ", "+")
    return [
        {
            "platform": "YouTube",
            "url": f"https://www.youtube.com/results?search_query={skill_lower}+tutorial",
            "is_free": True
        },
        {
            "platform": "Coursera",
            "url": f"https://www.coursera.org/search?query={skill_lower}",
            "is_free": False
        },
        {
            "platform": "freeCodeCamp",
            "url": f"https://www.freecodecamp.org/news/tag/{skill_lower}/",
            "is_free": True
        }
    ]
