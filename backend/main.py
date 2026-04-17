from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
from routers import auth, users, jobs, recommendations, upload


app = FastAPI(
    title="Smart Job Recommendation System",
    description="AI-powered job recommendations based on skill gap analysis",
    version="1.0.0"
)

app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected successfully")
    except Exception as e:
        print("Database connection failed:", e)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(recommendations.router)
app.include_router(upload.router)




@app.get("/")
def root():
    return {
        "message": "Smart Job Recommendation API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
