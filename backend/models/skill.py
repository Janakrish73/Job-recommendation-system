from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(
        Enum("programming", "database", "cloud", "ml", "soft", "other"),
        default="other"
    )
    description = Column(String(300), nullable=True)

    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")
    job_skills = relationship("JobSkill", back_populates="skill")
    resources = relationship("SkillResource", back_populates="skill", cascade="all, delete-orphan")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency = Column(
        Enum("beginner", "intermediate", "advanced"),
        default="intermediate"
    )

    __table_args__ = (UniqueConstraint("user_id", "skill_id"),)

    # Relationships
    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    is_required = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint("job_id", "skill_id"),)

    # Relationships
    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")


class SkillResource(Base):
    __tablename__ = "skill_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(100), nullable=True)
    url = Column(String(500), nullable=False)
    is_free = Column(Boolean, default=True)

    # Relationship
    skill = relationship("Skill", back_populates="resources")
