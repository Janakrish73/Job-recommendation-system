from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    remote = "remote"


class SkillBasic(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True


class JobSkillResponse(BaseModel):
    skill: SkillBasic
    is_required: bool

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    job_type: Optional[JobType] = JobType.full_time
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: Optional[str] = None
    skill_ids: Optional[List[int]] = []


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str] = None
    job_type: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    description: Optional[str] = None
    posted_at: Optional[datetime] = None
    is_active: bool
    job_skills: List[JobSkillResponse] = []

    class Config:
        from_attributes = True


class RecommendationResult(BaseModel):
    job_id: int
    title: str
    company: str
    location: Optional[str]
    job_type: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: Optional[str]
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    required_skills: List[str]


class RecommendationResponse(BaseModel):
    user_id: int
    user_name: str
    user_skills: List[str]
    total_jobs_analyzed: int
    recommendations: List[RecommendationResult]
