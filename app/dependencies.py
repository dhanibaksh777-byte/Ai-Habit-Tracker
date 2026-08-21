from app.Routers.auth import ALGORITHIM,SECRETE_KEY,Auth
from fastapi import HTTPException,status,Depends
from app.models import User
from app.database import get_db
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from uuid import UUID

def verify_token(token : str):
    try:
        payload = jwt.decode(token,SECRETE_KEY,algorithms=[ALGORITHIM])
        return payload

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token or session expired")

def get_current_user(token : str = Depends(Auth),db : Session = Depends(get_db)):
    payload = verify_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user not found in token")
    db_user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found!")
    return db_user