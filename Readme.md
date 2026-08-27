# AI Habit Tracker — Backend

A FastAPI backend for tracking daily habits, calculating streaks, and generating AI-powered weekly insights using Groq.

## Features

- **Authentication** — JWT-based auth with bcrypt password hashing
- **Habit Management** — Full CRUD for user habits
- **Daily Logging** — Mark habits as done/skipped per day (upsert pattern — no duplicate logs per day)
- **Streak Tracking** — Current streak and longest streak calculation
- **AI Insights** — Weekly summary and suggestions generated via Groq, based on the user's actual logged data
- **Rate Limiting** — Per-endpoint request limits (stricter on the AI insights endpoint)

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Migrations:** Alembic
- **Auth:** JWT (python-jose) + bcrypt
- **AI:** Groq API (`openai/gpt-oss-120b`)
- **Rate Limiting:** SlowAPI

## Project Structure

```
habit-tracker/
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── database.py          # DB engine, session, base
│   ├── models.py            # SQLAlchemy models (User, Habit, HabitLog)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── dependencies.py      # get_current_user auth dependency
│   ├── limiter.py           # Rate limiter instance
│   ├── routers/
│   │   ├── auth.py          # /register, /login
│   │   └── habits.py        # Habit CRUD, logs, streaks, insights
│   └── services/
│       └── ai_insights.py   # Groq integration for weekly insights
├── alembic/                 # Database migrations
├── requirements.txt
└── .env                     # Environment variables (not committed)
```

## Setup

1. **Clone the repo and create a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project root:
   ```
   database_url=postgresql://user:password@localhost/habit_tracker
   secret_key=your_generated_secret_key
   groq_api_key=your_groq_api_key
   ```
   Generate a secret key with:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Run migrations**
   ```
   alembic upgrade head
   ```

5. **Start the server**
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Log in and receive a JWT |

### Habits
| Method | Endpoint | Description |
|---|---|---|
| POST | `/habits` | Create a new habit |
| GET | `/habits` | List all habits for the current user |
| GET | `/habits/{habit_id}` | Get a single habit |
| PUT | `/habits/{habit_id}` | Update a habit |
| DELETE | `/habits/{habit_id}` | Delete a habit |

### Logs
| Method | Endpoint | Description |
|---|---|---|
| POST | `/habits/log/{habit_id}` | Mark today's status (done/skipped) — upserts |
| GET | `/habits/log/{habit_id}` | Get all logs for a habit |

### Streaks & Insights
| Method | Endpoint | Description |
|---|---|---|
| GET | `/habits/streak/{habit_id}` | Get current and longest streak |
| GET | `/habits/insights/{habit_id}` | Get an AI-generated weekly summary |

All habit/log/streak/insight endpoints require a `Bearer` token from `/auth/login`.

## Notes

- All timestamps are stored timezone-aware (UTC).
- The AI insights endpoint is intentionally rate-limited more tightly than other endpoints, since it triggers an external API call.
- Insights are generated strictly from the user's own logged data — the model is instructed not to invent information.

## Author

Bilal — [GitHub](https://github.com/dhanibaksh777-byte)