from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User, UserProfile
from models.skill import Skill, UserSkill
from schemas.user import ProfileCreate, ProfileResponse, UserSkillAdd, UserSkillResponse, UserResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the currently logged-in user's full profile."""
    return current_user


@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile (education, experience, location, etc.)."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/skills", response_model=List[UserSkillResponse])
def get_my_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all skills for the current user."""
    return current_user.user_skills


@router.post("/skills", response_model=UserSkillResponse, status_code=status.HTTP_201_CREATED)
def add_skill(
    skill_data: UserSkillAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a skill to the user's profile."""
    # Verify skill exists
    skill = db.query(Skill).filter(Skill.id == skill_data.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check if already added
    existing = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill_data.skill_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already added to your profile")

    user_skill = UserSkill(
        user_id=current_user.id,
        skill_id=skill_data.skill_id,
        proficiency=skill_data.proficiency
    )
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)
    return user_skill


@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a skill from the user's profile."""
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if not user_skill:
        raise HTTPException(status_code=404, detail="Skill not in your profile")

    db.delete(user_skill)
    db.commit()


@router.post("/skills/bulk")
def add_skills_bulk(
    skill_names: List[str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add multiple skills at once by name (used after resume upload)."""
    added = []
    skipped = []

    for name in skill_names:
        skill = db.query(Skill).filter(Skill.name.ilike(name)).first()
        if not skill:
            # Auto-create unknown skill
            skill = Skill(name=name.strip(), category="other")
            db.add(skill)
            db.flush()

        existing = db.query(UserSkill).filter(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_id == skill.id
        ).first()

        if not existing:
            user_skill = UserSkill(user_id=current_user.id, skill_id=skill.id)
            db.add(user_skill)
            added.append(name)
        else:
            skipped.append(name)

    db.commit()
    return {"added": added, "already_existed": skipped}
