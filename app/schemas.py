from pydantic import BaseModel,EmailStr

#USER SCHEMAS:
class CreateUser(BaseModel):
    username : str 
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    username : str

    class Config:
        from_attributes = True

#Habit schema

class CreateHabit(BaseModel):
    name : str 

class HabitResponse(BaseModel):
    id : str 
    name : str

    class Config(BaseModel):
        from_attributes = True


