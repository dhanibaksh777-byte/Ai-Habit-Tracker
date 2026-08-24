from app.dependencies import get_current_user
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.models import User,Habit,HabitLog
from app.schemas import CreateHabit,UpdatedHabit,HabitStatus
from app.database import get_db
from uuid import UUID
from datetime import date,timedelta


router = APIRouter(prefix="/habit")


@router.post("/create-habit")
def habit(habit : CreateHabit,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    new_habit = Habit(name = habit.name,user_id = CurrentUser.id)
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit


@router.get("/get-habit/{habit_id}")
def get_habit(habit_id : UUID,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
    return habit

@router.get("/get-all-habits")
def get_all_habits(CurrentUser : User = Depends(get_current_user), db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.user_id == CurrentUser.id).all()
    return habit

@router.patch("/update-habit/{habit_id}")
def update_habit(habit_id : UUID,update_habit : UpdatedHabit,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
    habit.name = update_habit.updated_name
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return {"message" : "habit updated successfully!"}



@router.delete("/delete-habit/{habit_id}")
def delete_habit(habit_id : UUID,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
    db.delete(habit)
    db.commit()
    return {"message" : "habit deleted successfully!"}


@router.get("/streak/{habit_id}")
def streak_count(habit_id : UUID,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
     habit = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
     if not habit :
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habit not found!")
     logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.date.desc()).all()
     current_streak = 0
     expected_date = date.today()

     for log in logs:
          if log.date == expected_date or log.status == HabitStatus.DONE:
               current_streak += 1
               expected_date -= timedelta(days=1)
          else:
            break

     logs_ascending = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).order_by(HabitLog.date.asc()).all()
     longest_streak = 0
     temp_streak = 0
     previous_date = None

     for logs in logs_ascending:
         if logs.status != HabitStatus.DONE:
             temp_streak = 0

            
         elif logs.status ==  HabitStatus.Done:
             if previous_date is not None and logs.date == previous_date + timedelta(days=1):
                 temp_streak += 1
                 longest_streak = max(longest_streak,temp_streak)

         previous_date = logs.date

             

             
             
             
         
     


     