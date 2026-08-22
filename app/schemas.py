from pydantic import BaseModel,EmailStr
from uuid import UUID
#USER SCHEMAS:
class CreateUser(BaseModel):
    username : str 
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : UUID
    username : str

    class Config:
        from_attributes = True

#Habit schema

class CreateHabit(BaseModel):
    name : str 

class HabitResponse(BaseModel):
    id : UUID
    name : str

    class Config:
        from_attributes = True

class UpdatedHabit(BaseModel):
    updated_name : str

