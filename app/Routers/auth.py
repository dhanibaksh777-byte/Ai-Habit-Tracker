from app.database import get_db
from fastapi import APIRouter,Depends,HTTPException,status
from app.models import User
from jose import jwt
import bcrypt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas import CreateUser,UserLogin,UserResponse
from dotenv import load_dotenv
from datetime import datetime,timezone
from typing import Any
import os 

load_dotenv()

Auth = OAuth2PasswordBearer(tokenUrl="auth/login")


SECRETE_KEY = os.getenv("secrete_key")
if not SECRETE_KEY:
    raise RuntimeError("secrete_key missing in .env file")

ALGORITHIM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

def hash_password(plain_password : str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode("utf-8"),salt).decode("utf-8")

def create_token(data : dict[str,Any]):
    Expire = datetime.now(timezone.utc)
    payload = data.copy()
    payload.update({"expire":Expire})
    token = jwt.encode(payload,SECRETE_KEY,algorithm=ALGORITHIM)
    return token

router = APIRouter(prefix="/auth")


@router.post("/register",status_code=status.HTTP_201_CREATED)
def regester(user : CreateUser,db : Session = Depends(get_db)):
    username = db.query(User).filter(User.username == user.username).first()
    if username:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail="username already exists")
    email = db.query(User).filter(User.email == user.email).first()
    if email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username = user.username,email = user.email,hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user : UserLogin,db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"),db_user.password.encode("utf-8")):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="wrong password email")
    token = create_token({"user_id" : db_user.id})
    return {"token" : token,"token_type" : "Bearer"}





    



    








