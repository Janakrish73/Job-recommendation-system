from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.job import Job
from models.skill import Skill, JobSkill
from schemas.job import JobCreate, JobResponse
from schemas.user import SkillResponse
from utils.auth import get_current_user

router = APIRouter(tags=["Jobs"])


# ── Skills Master List ────────────────────────────────────────────────────────

@router.get("/skills", response_model=List[SkillResponse])
def get_all_skills(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all available skills. Optionally filter by category."""
    query = db.query(Skill)
    if category:
        query = query.filter(Skill.category == category)
    return query.order_by(Skill.name).all()


@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    name: str,
    category: str = "other",
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new skill in the master list."""
    existing = db.query(Skill).filter(Skill.name.ilike(name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    skill = Skill(name=name.strip(), category=category, description=description)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


# ── Jobs ──────────────────────────────────────────────────────────────────────

@router.get("/jobs", response_model=List[JobResponse])
def get_jobs(
    search: Optional[str] = Query(None, description="Search by job title or company"),
    job_type: Optional[str] = None,
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all active job listings with optional filters."""
    query = db.query(Job).filter(Job.is_active == True)

    if search:
        query = query.filter(
            (Job.title.ilike(f"%{search}%")) |
            (Job.company.ilike(f"%{search}%"))
        )
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    return query.order_by(Job.posted_at.desc()).offset(skip).limit(limit).all()


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a single job by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """Create a new job listing with required skills."""
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        job_type=job_data.job_type,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        description=job_data.description,
    )
    db.add(job)
    db.flush()

    # Add required skills
    for skill_id in job_data.skill_ids or []:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if skill:
            job_skill = JobSkill(job_id=job.id, skill_id=skill_id, is_required=True)
            db.add(job_skill)

    db.commit()
    db.refresh(job)
    return job


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Soft-delete a job (sets is_active = False)."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.is_active = False
    db.commit()
