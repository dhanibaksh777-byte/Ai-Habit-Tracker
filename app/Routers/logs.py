from fastapi import APIRouter,Depends,HTTPException,status
from app.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.models import HabitStatus,Habit,HabitLog
from app.models import User
from app.schemas import CreateLog,LogResponse
from uuid import UUID
from app.database import get_db
from datetime import date



router = APIRouter(prefix="/habits",tags=["logs"])



@router.post("/log/{habit_id}")
def log(habit_id : UUID,log : CreateLog,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
    today = date.today()
    existing_log = db.query(HabitLog).filter(HabitLog.habit_id == habit_id,HabitLog.date == today).first()
    if existing_log:
        existing_log.status = log.status

    else:
        existing_log = HabitLog(habit_id = habit_id,date = today,status = log.status)

    db.add(existing_log)
    db.commit()
    db.refresh(existing_log)
    return existing_log


@router.get("/log/{habit_id}")
def get_all_logs(habit_id : UUID,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
    log = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).all()
    return log