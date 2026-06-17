# AI-Powered Distance Learning Management System

A production-grade, AI-powered LMS with intelligent course generation, learning analytics, and real-time collaboration.

## Features
- **AI-Powered:** Course/Quiz/Exam generation, AI Tutor, and Study Recommendations.
- **Real-Time Collaboration:** Group and Private Chat using SocketIO.
- **Academic Hierarchy:** Faculty -> Department -> Programme -> Level -> Session -> Semester -> Subject -> Course.
- **Modules:** Assignment submission, CBT Examinations, Certificate generation.
- **Analytics:** Performance dashboards for Students, Lecturers, and Admins.

## Tech Stack
- **Backend:** Python 3.13+, Flask, Flask-SQLAlchemy, Celery, Redis.
- **Frontend:** HTML5, Tailwind CSS, Alpine JS, Chart.js.
- **AI:** Gemini API.

## Setup
1.  **Environment Variables:** Create a `.env` file with `DATABASE_URL`, `GEMINI_API_KEY`, and `REDIS_URL`.
2.  **Docker:** Run `docker-compose up --build`.
3.  **Migrations:** `flask db upgrade` to initialize the database.
