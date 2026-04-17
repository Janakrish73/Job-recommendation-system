# ⚡ Smart Job Recommendation System
### MSc Computer Science Final Year Project

A full-stack web application that recommends jobs based on your skills using **cosine similarity**, **TF-IDF matching**, and **NLP-powered resume parsing**.

---

## 🗂️ Project Structure

```
job_recommender/
├── backend/                  ← Python FastAPI backend
│   ├── main.py               ← App entry point
│   ├── database.py           ← MySQL connection
│   ├── setup_database.sql    ← SQL to create all tables
│   ├── seed_data.py          ← Populate with sample data
│   ├── requirements.txt      ← Python dependencies
│   ├── .env.example          ← Environment variable template
│   ├── models/               ← SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── skill.py
│   │   └── job.py
│   ├── schemas/              ← Pydantic request/response schemas
│   │   ├── user.py
│   │   └── job.py
│   ├── routers/              ← API route handlers
│   │   ├── auth.py           ← /auth/register, /auth/login
│   │   ├── users.py          ← /users/me, /users/profile, /users/skills
│   │   ├── jobs.py           ← /jobs, /skills
│   │   ├── recommendations.py ← /recommend/me, /recommend/gap/{id}
│   │   └── upload.py         ← /upload/resume
│   ├── services/             ← Business logic
│   │   ├── matcher.py        ← Cosine similarity + TF-IDF engine
│   │   └── skill_extractor.py ← NLP skill extraction
│   └── utils/
│       ├── auth.py           ← JWT & password hashing
│       └── pdf_parser.py     ← PDF text extraction
└── frontend/
    └── index.html            ← Complete single-page app (no build needed!)
```

---

## ⚙️ Setup Instructions

### Step 1 — Install MySQL
Download MySQL Community Server from https://dev.mysql.com/downloads/

### Step 2 — Create the database
```bash
mysql -u root -p < backend/setup_database.sql
```

### Step 3 — Set up Python environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4 — Configure environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your MySQL credentials
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/job_recommender
SECRET_KEY=your_random_secret_key_here
```

### Step 5 — Seed the database with sample data
```bash
python seed_data.py
```
This inserts 45+ skills, 10 jobs, and learning resources.

### Step 6 — Start the backend
```bash
uvicorn main:app --reload
```
API runs at: http://localhost:8000
API docs at: http://localhost:8000/docs ← Interactive!

### Step 7 — Open the frontend
Open `frontend/index.html` in your browser.
> If CORS issues occur, serve it: `python -m http.server 5500` from the frontend folder

---

## 🚀 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /auth/register | Create account |
| POST | /auth/login | Login, get JWT token |
| GET | /users/me | Get my profile |
| PUT | /users/profile | Update profile |
| GET | /users/skills | Get my skills |
| POST | /users/skills | Add a skill |
| DELETE | /users/skills/{id} | Remove a skill |
| POST | /users/skills/bulk | Add multiple skills at once |
| GET | /skills | All available skills |
| GET | /jobs | All job listings |
| GET | /jobs/{id} | Single job |
| POST | /jobs | Create job |
| GET | /recommend/me | Get ranked recommendations |
| GET | /recommend/gap/{job_id} | Skill gap for a specific job |
| POST | /upload/resume | Upload PDF resume |

---

## 🧠 How the Recommendation Engine Works

1. **User skills** are fetched from the database (e.g., ["Python", "SQL", "Flask"])
2. **Job required skills** are fetched for all active jobs
3. For each job, we compute:
   - **Set-based score** = matched skills / required skills × 100
   - **TF-IDF cosine similarity** = vectorize both skill sets, measure angle
   - **Final score** = 60% × set score + 40% × TF-IDF score
4. Jobs are **sorted descending** by final score
5. **Missing skills** = job required skills − user skills

---

## 📄 Resume Upload Flow

1. User uploads a PDF file
2. `pdfplumber` extracts all text
3. `skill_extractor.py` scans for 80+ known skill keywords using regex
4. Optionally enhanced with `spaCy` NER for technology names
5. Matched skills are auto-added to the user's profile

---

## ☁️ Deployment

### Backend → Railway
1. Push code to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add MySQL plugin
4. Set environment variables (DATABASE_URL, SECRET_KEY)
5. Add start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend → Vercel / Netlify
1. Edit `frontend/index.html`: Change `const API = 'http://localhost:8000'` to your Railway URL
2. Drag and drop the `frontend/` folder to Vercel or Netlify

---

## 🧪 Testing

Visit http://localhost:8000/docs for interactive Swagger UI testing of all endpoints.

---

## 🔑 Viva Keywords to Know

- **Cosine Similarity** — measures angle between skill vectors
- **TF-IDF** — Term Frequency-Inverse Document Frequency for weighted matching
- **JWT** — JSON Web Token for stateless authentication
- **bcrypt** — password hashing algorithm
- **SQLAlchemy** — Python ORM for database access
- **pdfplumber** — PDF text extraction library
- **spaCy** — NLP library for named entity recognition
- **Skill Gap** — required skills minus user skills
