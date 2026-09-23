## 🚀 Live Demo
[Click here to use the app](https://resume-analyzer-s5f4.vercel.app/)
# Resume_Analyzer
AI Resume Analyzer
# 🚀 AI Resume Analyzer

A full-stack web application that analyzes resumes against job descriptions and provides skill match insights.

## 🛠 Tech Stack

* Frontend: React + Tailwind CSS
* Backend: Python (FastAPI)
* Logic: LLM-driven evaluation (OpenAI) — real PDF/DOCX parsing + AI scoring and skill roadmap generation

## ✨ Features

* Resume vs Job Description analysis, evaluated by an LLM agent
* Skill matching & missing skills detection
* AI-generated recommended learning path for missing skills
* Clean cyberpunk UI

## 🚀 How to Run

### Backend

cd server_py
python -m venv venv
venv\Scripts\activate   (Windows) or source venv/bin/activate (macOS/Linux)
pip install -r requirements.txt
copy .env.example .env   # then fill in OPENAI_API_KEY
uvicorn main:app --reload --port 5000

### Frontend

cd client
npm install
npm run dev

## 📌 Future Improvements

* Advanced NLP / prompt tuning
* Authentication system
