# Smart Resume Screening System

**Smart Resume Screening System** — an end-to-end college project demonstrating a resume screening pipeline using React (frontend), Flask (backend), MySQL (database), and basic NLP/ML (TF-IDF + cosine similarity). The app accepts multiple resumes and ranks them against a job role, returning a score (0–10) and top candidates.

---

## Features

- Modern responsive React frontend (glassmorphism styling)
- Two-step registration + login flow
- Dashboard to upload multiple resumes (PDF/DOCX)
- Enter job role and number of openings
- Backend extracts text from resumes, cleans text (lemmatization, stopwords removal), vectorizes via TF-IDF, computes cosine similarity, scales scores to 0–10, and returns ranked candidates
- MySQL database to persist users, resumes, and results
- Sample resumes included for testing

---

## Setup Instructions

See `backend/README_BACKEND.md` and `frontend/README_FRONTEND.md` for step-by-step instructions.

