from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EducationLevel(str, Enum):
    high_school = "high_school"
    bachelors = "bachelors"
    masters = "masters"
    phd = "phd"


class Proficiency(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# ── Auth Schemas ─────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    full_name: str


# ── Profile Schemas ───────────────────────────────────────────────────────────

class ProfileCreate(BaseModel):
    education_level: Optional[EducationLevel] = EducationLevel.bachelors
    field_of_study: Optional[str] = None
    years_experience: Optional[int] = 0
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    bio: Optional[str] = None


class ProfileResponse(ProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ── Skill Schemas ─────────────────────────────────────────────────────────────

class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserSkillAdd(BaseModel):
    skill_id: int
    proficiency: Optional[Proficiency] = Proficiency.intermediate


class UserSkillResponse(BaseModel):
    id: int
    skill: SkillResponse
    proficiency: str

    class Config:
        from_attributes = True


# ── User Response ─────────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    resume_path: Optional[str] = None
    created_at: Optional[datetime] = None
    profile: Optional[ProfileResponse] = None
    user_skills: Optional[List[UserSkillResponse]] = []

    class Config:
        from_attributes = True
