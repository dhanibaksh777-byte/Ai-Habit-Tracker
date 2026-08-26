from groq import Groq
from dotenv import load_dotenv
import os
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import date,timedelta
from app.models import HabitLog

SYSTEM_PROMPT = """You are a supportive habit-building coach. You will be given a user's habit tracking data for the past 7 days (dates with status: done or skipped).

Your job:
- Write a short, encouraging summary (3-4 sentences max) of their week
- Point out patterns if any (e.g. specific days they tend to skip)
- End with one small, practical suggestion for next week
- Keep the tone warm and motivating, never guilt-tripping or harsh
- Do not invent data that wasn't given to you — only comment on what's in the log

Keep the entire response under 100 words."""


load_dotenv()

api_key = os.getenv("groq_api_key")
if not api_key:
    raise RuntimeError("api key did'nt found in .env file")
client = Groq(api_key=api_key)
def get_response(message : str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role" : "system", "content" : SYSTEM_PROMPT},
                  {"role" : "user","content" : message}],
        reasoning_effort="low"
        
    )
    return response.choices[0].message.content


def get_weekly_insights(habit_id : UUID,db : Session):
    week_ago = date.today() - timedelta(days=7)
    logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id,HabitLog.date >= week_ago).order_by(HabitLog.date.asc()).all()
    if not logs:
        return "No activity logged this week yet. Start logging to get insights!"
    log_lines = []
    for log in logs:
        line = f"{log.date} : {log.status.value}"
        log_lines.append(line)

    log_text = "\n".join(log_lines)
    insight = get_response(log_text)
    return insight


