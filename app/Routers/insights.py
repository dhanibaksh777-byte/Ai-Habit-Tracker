from app.services.ai_insights import get_weekly_insights
from uuid import UUID 
from app.database import get_db
from app.models import Habit,User
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.limiter import limiter
from fastapi import Request


router = APIRouter()


@router.get("/insights/{habit_id}")
@limiter.limit("10/day")
def get_insights(request : Request,habit_id : UUID,CurrentUser : User = Depends(get_current_user),db : Session = Depends(get_db)):
    habits = db.query(Habit).filter(Habit.id == habit_id,Habit.user_id == CurrentUser.id).first()
    if not habits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="habits not found!")

    insight = get_weekly_insights(habit_id,db)
    return {"insight" : insight}


