# AI Resume Analyzer

## Live Demo
[Click here to use the app](https://resume-analyzer-s5f4.vercel.app/)

A full-stack web app that scores a resume against a job description using an LLM, lists matched and missing skills, and suggests a learning path for the gaps. Users sign up and log in; accounts are stored in a database.

## Tech Stack

* **Frontend:** React + Vite + Tailwind CSS
* **Backend:** Python, Flask REST API
* **Database:** SQLite locally (Postgres on deploy) via Flask-SQLAlchemy
* **Auth:** hashed passwords + JWT bearer tokens
* **AI:** OpenRouter LLM (OpenAI SDK), PDF/DOCX/TXT parsing with pypdf and python-docx

## How It Works

1. **Sign up / log in.** The React auth modal calls `POST /api/auth/signup` or `/api/auth/login`. The backend stores the email and a hashed password in the `users` table, then returns a signed JWT. The browser keeps the token, so a refresh keeps you logged in (`GET /api/auth/me`).
2. **Submit.** On the analyzer page you upload a resume (.pdf, .docx, .txt) or paste text, add a job description, and send it to `POST /api/analyze` with the token. Requests without a valid token get a 401.
3. **Parse.** The backend extracts the resume text from the file.
4. **Size guard.** Resume text is capped at 20,000 characters and the job description at 10,000. Longer text is truncated with a warning. Everything goes to the LLM as one request (no chunking).
5. **Analyze.** The LLM returns JSON: match score, summary, matched and missing skills, skill bars, and a learning path per missing skill. The output is validated before it is sent back.
6. **Display.** The frontend shows the score ring, skill bars and recommendations.

On startup the backend terminal prints a banner describing the endpoints, auth flow and pipeline. Every request is then logged stage by stage (receive, parse, budget, LLM call, JSON parse) with a request id, character counts and estimated tokens. Passwords are never logged.

## API

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/signup` | no | Create account, returns token |
| POST | `/api/auth/login` | no | Verify credentials, returns token |
| GET | `/api/auth/me` | token | Current user |
| POST | `/api/analyze` | token | Analyze resume vs job description |
| GET | `/health` | no | Health check |

## Project Structure

```
client/                 React app (pages/, components/, services/api.js)
server_py/
  app.py                Flask app, request logging, error handling
  database.py           SQLAlchemy setup + User model
  logging_config.py     Startup banner, log format, size limits
  routes/               auth.py, analyze.py
  services/             auth_service.py, file_parser.py, llm_service.py
  models/schemas.py     Response validation
```

## How to Run

### Backend

```
cd server_py
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # then fill in the values below
python app.py
```

Required `.env` values:

| Variable | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | LLM access |
| `JWT_SECRET` | Signs login tokens. Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |

Optional: `OPENROUTER_MODEL`, `PORT` (5000), `DATABASE_URL` (defaults to local SQLite), `JWT_EXPIRES_HOURS` (24), `CORS_ORIGINS`, `MAX_RESUME_CHARS`, `MAX_JD_CHARS`, `LOG_LEVEL`.

The database tables are created automatically on first start.

### Frontend

```
cd client
npm install
copy .env.example .env         # VITE_API_URL=http://localhost:5000
npm run dev
```

### Deploy (Render)

Start command: `gunicorn app:app`. Set the environment variables above, and use a Postgres `DATABASE_URL` (uncomment `psycopg2-binary` in requirements.txt) because Render's local disk is wiped on redeploy.

## Future Improvements

* Save each user's past analyses
* Password reset and email verification
* Rate limiting on login and analyze
