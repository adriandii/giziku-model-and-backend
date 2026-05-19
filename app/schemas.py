from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MealRequest(BaseModel):
    food: str
    amount: float

class ProfileRequest(BaseModel):
    sex: str
    age: int
    weight: float
    height: float

    activity_level: str
    exercise_level: str
    target: str