"""
Seed the database with sample skills, jobs, and skill resources.
Run: python seed_data.py
"""
#seed_data.py

from database import SessionLocal, engine, Base
from models.user import User, UserProfile
from models.skill import Skill, JobSkill, SkillResource
from models.job import Job

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_skills():
    print("Seeding skills...")
    skills_data = [
        # Programming
        ("Python", "programming", "General-purpose programming language"),
        ("JavaScript", "programming", "Web scripting language"),
        ("TypeScript", "programming", "Typed superset of JavaScript"),
        ("Java", "programming", "Object-oriented language"),
        ("Go", "programming", "Compiled, statically typed language by Google"),
        ("C++", "programming", "High-performance systems language"),
        ("PHP", "programming", "Server-side scripting language"),
        ("Ruby", "programming", "Dynamic scripting language"),

        # Web
        ("React", "programming", "JavaScript UI library by Facebook"),
        ("Angular", "programming", "TypeScript-based web framework"),
        ("Vue", "programming", "Progressive JavaScript framework"),
        ("HTML", "programming", "Web markup language"),
        ("CSS", "programming", "Web styling language"),
        ("FastAPI", "programming", "Modern Python web framework"),
        ("Django", "programming", "Full-stack Python web framework"),
        ("Flask", "programming", "Lightweight Python web framework"),
        ("Node.js", "programming", "JavaScript runtime for backend"),
        ("REST API", "programming", "HTTP API design pattern"),
        ("GraphQL", "programming", "Query language for APIs"),

        # Database
        ("SQL", "database", "Structured Query Language"),
        ("MySQL", "database", "Open-source relational database"),
        ("PostgreSQL", "database", "Advanced open-source relational database"),
        ("MongoDB", "database", "NoSQL document database"),
        ("Redis", "database", "In-memory data store and cache"),

        # Cloud & DevOps
        ("Docker", "cloud", "Container platform"),
        ("Kubernetes", "cloud", "Container orchestration"),
        ("AWS", "cloud", "Amazon Web Services cloud platform"),
        ("Azure", "cloud", "Microsoft cloud platform"),
        ("GCP", "cloud", "Google Cloud Platform"),
        ("Git", "cloud", "Version control system"),
        ("CI/CD", "cloud", "Continuous integration and deployment"),
        ("Linux", "cloud", "Open-source operating system"),

        # ML & Data Science
        ("Machine Learning", "ml", "Building systems that learn from data"),
        ("Deep Learning", "ml", "Neural network-based machine learning"),
        ("NLP", "ml", "Natural Language Processing"),
        ("TensorFlow", "ml", "Open-source ML framework by Google"),
        ("PyTorch", "ml", "Open-source ML framework by Meta"),
        ("scikit-learn", "ml", "Python ML library"),
        ("Pandas", "ml", "Python data analysis library"),
        ("NumPy", "ml", "Numerical computing library"),
        ("Data Analysis", "ml", "Analyzing data to extract insights"),
        ("Data Science", "ml", "Extracting knowledge from data"),
        ("Power BI", "ml", "Microsoft business intelligence tool"),
        ("Tableau", "ml", "Data visualization platform"),

        # Soft Skills
        ("Communication", "soft", "Effective verbal and written communication"),
        ("Teamwork", "soft", "Collaborating effectively in a team"),
        ("Agile", "soft", "Iterative software development methodology"),
        ("Scrum", "soft", "Agile framework for project management"),
        ("Problem Solving", "soft", "Analytical thinking to solve problems"),
    ]

    for name, category, description in skills_data:
        existing = db.query(Skill).filter(Skill.name == name).first()
        if not existing:
            db.add(Skill(name=name, category=category, description=description))

    db.commit()
    print(f"  Success {len(skills_data)} skills seeded")


def seed_jobs():
    print("Seeding jobs...")

    def get_skill_id(name):
        s = db.query(Skill).filter(Skill.name == name).first()
        return s.id if s else None

    jobs_data = [
        {
            "title": "Junior Python Developer",
            "company": "TechCorp Solutions",
            "location": "Remote",
            "job_type": "full_time",
            "salary_min": 40000,
            "salary_max": 60000,
            "description": "Build and maintain Python microservices. Work with REST APIs and MySQL databases. Collaborate with a small agile team. Great opportunity for new graduates.",
            "skills": ["Python", "SQL", "MySQL", "REST API", "Git", "Flask"],
        },
        {
            "title": "Data Analyst",
            "company": "DataSoft Analytics",
            "location": "New York, NY",
            "job_type": "full_time",
            "salary_min": 55000,
            "salary_max": 80000,
            "description": "Analyze large datasets, create dashboards and reports. Work closely with business teams to deliver insights. Experience with SQL, Python and data visualization tools required.",
            "skills": ["SQL", "Python", "Pandas", "Data Analysis", "Power BI", "Tableau"],
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Labs Inc",
            "location": "San Francisco, CA",
            "job_type": "full_time",
            "salary_min": 90000,
            "salary_max": 130000,
            "description": "Design and deploy machine learning models at scale. Experience with deep learning frameworks required. You'll work on NLP and computer vision projects.",
            "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "scikit-learn", "Docker"],
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": "London, UK",
            "job_type": "full_time",
            "salary_min": 65000,
            "salary_max": 95000,
            "description": "Build full-stack web apps with React frontend and Python FastAPI backend. Must be comfortable with Docker and cloud deployment. Agile team environment.",
            "skills": ["Python", "React", "FastAPI", "Docker", "PostgreSQL", "Git", "REST API"],
        },
        {
            "title": "Backend Developer Intern",
            "company": "FinTech Innovations",
            "location": "Remote",
            "job_type": "internship",
            "salary_min": 15000,
            "salary_max": 25000,
            "description": "Join our backend team and assist with Python development. Learn Django and REST API design in a real-world environment. Ideal for students or recent graduates.",
            "skills": ["Python", "Django", "SQL", "Git", "REST API"],
        },
        {
            "title": "React Frontend Developer",
            "company": "WebAgency Creative",
            "location": "Austin, TX",
            "job_type": "full_time",
            "salary_min": 60000,
            "salary_max": 85000,
            "description": "Create beautiful, responsive React applications. Work with UI/UX designers and backend teams. Strong JavaScript and CSS skills required.",
            "skills": ["JavaScript", "React", "TypeScript", "HTML", "CSS", "Git", "REST API"],
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudBase Systems",
            "location": "Remote",
            "job_type": "remote",
            "salary_min": 80000,
            "salary_max": 120000,
            "description": "Manage cloud infrastructure, set up CI/CD pipelines, and ensure high availability. Experience with Docker, Kubernetes, and AWS required.",
            "skills": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD", "Python", "Git"],
        },
        {
            "title": "Data Science Intern",
            "company": "BioAnalytics Corp",
            "location": "Boston, MA",
            "job_type": "internship",
            "salary_min": 18000,
            "salary_max": 28000,
            "description": "Assist data science team with exploratory analysis, model building, and data visualization. A great chance to apply your machine learning knowledge.",
            "skills": ["Python", "Pandas", "NumPy", "scikit-learn", "Data Analysis", "SQL"],
        },
        {
            "title": "NLP Research Engineer",
            "company": "LanguageAI",
            "location": "Remote",
            "job_type": "full_time",
            "salary_min": 95000,
            "salary_max": 140000,
            "description": "Research and implement NLP models for text classification, entity extraction, and summarization. Strong Python and deep learning background required.",
            "skills": ["Python", "NLP", "Deep Learning", "PyTorch", "Machine Learning", "Data Science"],
        },
        {
            "title": "Database Administrator",
            "company": "Enterprise Systems Ltd",
            "location": "Chicago, IL",
            "job_type": "full_time",
            "salary_min": 65000,
            "salary_max": 95000,
            "description": "Manage and optimize relational databases. Ensure data integrity, performance, and security. Strong SQL and PostgreSQL skills required.",
            "skills": ["SQL", "MySQL", "PostgreSQL", "Redis", "Python", "Linux"],
        },
    ]

    for job_data in jobs_data:
        existing = db.query(Job).filter(
            Job.title == job_data["title"],
            Job.company == job_data["company"]
        ).first()
        if existing:
            continue

        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            job_type=job_data["job_type"],
            salary_min=job_data["salary_min"],
            salary_max=job_data["salary_max"],
            description=job_data["description"],
        )
        db.add(job)
        db.flush()

        for skill_name in job_data["skills"]:
            skill_id = get_skill_id(skill_name)
            if skill_id:
                db.add(JobSkill(job_id=job.id, skill_id=skill_id, is_required=True))

    db.commit()
    print(f"  Success {len(jobs_data)} jobs seeded")


def seed_resources():
    print("Seeding skill resources...")
    resources = [
        ("Python", "YouTube", "https://www.youtube.com/watch?v=_uQrJ0TkZlc", True),
        ("Python", "freeCodeCamp", "https://www.freecodecamp.org/learn/scientific-computing-with-python/", True),
        ("React", "YouTube", "https://www.youtube.com/watch?v=bMknfKXIFA8", True),
        ("React", "Official Docs", "https://react.dev/learn", True),
        ("Machine Learning", "Coursera", "https://www.coursera.org/learn/machine-learning", False),
        ("Machine Learning", "YouTube", "https://www.youtube.com/watch?v=gmvvaobm7eQ", True),
        ("SQL", "SQLZoo", "https://sqlzoo.net/wiki/SQL_Tutorial", True),
        ("Docker", "Official Docs", "https://docs.docker.com/get-started/", True),
        ("Docker", "YouTube", "https://www.youtube.com/watch?v=gAkwW2tuIqE", True),
        ("AWS", "AWS Free Tier", "https://aws.amazon.com/free/", True),
        ("FastAPI", "Official Docs", "https://fastapi.tiangolo.com/", True),
        ("Django", "Official Tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/", True),
    ]

    for skill_name, platform, url, is_free in resources:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if skill:
            existing = db.query(SkillResource).filter(
                SkillResource.skill_id == skill.id,
                SkillResource.url == url
            ).first()
            if not existing:
                db.add(SkillResource(skill_id=skill.id, platform=platform, url=url, is_free=is_free))

    db.commit()
    print(f"  Success {len(resources)} resources seeded")


if __name__ == "__main__":
    print(" Starting database seed...")
    seed_skills()
    seed_jobs()
    seed_resources()
    print("Database seeded successfully!")
    print("\nYou can now run: uvicorn main:app --reload")
    db.close()
