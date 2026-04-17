from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil, os

from database import get_db
from models.user import User
from models.skill import Skill, UserSkill
from utils.auth import get_current_user
from utils.pdf_parser import extract_text_from_pdf
from services.skill_extractor import extract_skills_from_text

router = APIRouter(prefix="/upload", tags=["Resume Upload"])

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {"application/pdf"}
MAX_SIZE_MB = 5


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a PDF resume.
    Automatically extracts skills using NLP and adds them to your profile.
    """
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read file and validate size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File too large. Max size is {MAX_SIZE_MB}MB.")

    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"user_{current_user.id}_resume.pdf"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    # Update user resume path
    current_user.resume_path = filepath
    db.commit()

    # Extract text and skills
    text = extract_text_from_pdf(filepath)
    if not text:
        return {
            "message": "Resume uploaded but could not extract text. Please add skills manually.",
            "resume_path": filepath,
            "extracted_skills": [],
            "added_skills": [],
        }

    extracted_skills = extract_skills_from_text(text)

    # Save extracted skills to user profile
    added_skills = []
    for skill_name in extracted_skills:
        # Find or create skill
        skill = db.query(Skill).filter(Skill.name.ilike(skill_name)).first()
        if not skill:
            skill = Skill(name=skill_name, category="other")
            db.add(skill)
            db.flush()

        # Add to user if not already there
        existing = db.query(UserSkill).filter(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_id == skill.id
        ).first()

        if not existing:
            user_skill = UserSkill(user_id=current_user.id, skill_id=skill.id)
            db.add(user_skill)
            added_skills.append(skill_name)

    db.commit()

    return {
        "message": f"Resume processed successfully! Found {len(extracted_skills)} skills, added {len(added_skills)} new ones.",
        "resume_path": filepath,
        "extracted_skills": extracted_skills,
        "added_skills": added_skills,
        "already_existed": [s for s in extracted_skills if s not in added_skills],
    }


@router.get("/resume/text")
def get_resume_text(
    current_user: User = Depends(get_current_user)
):
    """Get extracted text from the user's uploaded resume."""
    if not current_user.resume_path or not os.path.exists(current_user.resume_path):
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")

    text = extract_text_from_pdf(current_user.resume_path)
    return {"text_preview": text[:2000], "total_chars": len(text)}
