--Running command
-- mysql -u root -p < setup_database.sql



CREATE DATABASE IF NOT EXISTS job_recommender CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE job_recommender;

-- ── 1. Users
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    email        VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name    VARCHAR(100) NOT NULL,
    resume_path  VARCHAR(500),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- ── 2. User Profiles 
CREATE TABLE IF NOT EXISTS user_profiles (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT NOT NULL UNIQUE,
    education_level  ENUM('high_school','bachelors','masters','phd') DEFAULT 'bachelors',
    field_of_study   VARCHAR(100),
    years_experience INT DEFAULT 0,
    location         VARCHAR(100),
    linkedin_url     VARCHAR(300),
    bio              TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── 3. Skills Master 
CREATE TABLE IF NOT EXISTS skills (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    category    ENUM('programming','database','cloud','ml','soft','other') DEFAULT 'other',
    description VARCHAR(300),
    INDEX idx_name (name)
);

-- ── 4. User Skills 
CREATE TABLE IF NOT EXISTS user_skills (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    skill_id    INT NOT NULL,
    proficiency ENUM('beginner','intermediate','advanced') DEFAULT 'intermediate',
    UNIQUE KEY unique_user_skill (user_id, skill_id),
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- ── 5. Jobs 
CREATE TABLE IF NOT EXISTS jobs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    company     VARCHAR(200) NOT NULL,
    location    VARCHAR(100),
    job_type    ENUM('full_time','part_time','internship','remote') DEFAULT 'full_time',
    salary_min  INT,
    salary_max  INT,
    description TEXT,
    posted_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active   BOOLEAN DEFAULT TRUE,
    INDEX idx_active (is_active),
    FULLTEXT INDEX idx_search (title, company)
);

-- ── 6. Job Skills 
CREATE TABLE IF NOT EXISTS job_skills (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    job_id      INT NOT NULL,
    skill_id    INT NOT NULL,
    is_required BOOLEAN DEFAULT TRUE,
    UNIQUE KEY unique_job_skill (job_id, skill_id),
    FOREIGN KEY (job_id)   REFERENCES jobs(id)   ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- ── 7. Applications 
CREATE TABLE IF NOT EXISTS job_applications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    job_id      INT NOT NULL,
    match_score DECIMAL(5,2),
    status      ENUM('applied','reviewing','interview','rejected','accepted') DEFAULT 'applied',
    applied_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_application (user_id, job_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id)  REFERENCES jobs(id)  ON DELETE CASCADE
);

-- ── 8. Skill Resources 
CREATE TABLE IF NOT EXISTS skill_resources (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    skill_id  INT NOT NULL,
    platform  VARCHAR(100),
    url       VARCHAR(500) NOT NULL,
    is_free   BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

SELECT 'Database setup complete! Run: python seed_data.py' AS status;
