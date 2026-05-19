from fastapi import FastAPI, UploadFile, File
from app.model import predict_image
from app.nutrition import calculate_nutrition
from app.schemas import MealRequest
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

from app.schemas import UserRegister, UserLogin, MealRequest
from app.database import engine
from app.models import Base, Food
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Meal
from app.models import UserProfile
from app.schemas import ProfileRequest
from app.macro import calculate_daily_targets
from datetime import date
from sqlalchemy import func

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBearer()

# simple in-memory storage
meals = []

@app.get("/")
def root():
    return {"message": "Food Nutrition API running"}



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Username atau Password salah")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Username atau Password salah")

    token = create_access_token({
        "sub": db_user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/profile")
def create_profile(
    request: ProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    targets = calculate_daily_targets(
        weight=request.weight,
        height=request.height,
        age=request.age,
        sex=request.sex,
        target=request.target,
        activity_level=request.activity_level,
        exercise_level=request.exercise_level
    )

    profile = UserProfile(
        age=request.age,
        weight=request.weight,
        height=request.height,

        sex=request.sex,
        target=request.target,
        activity_level=request.activity_level,
        exercise_level=request.exercise_level,

        target_calories=targets["calories"],
        target_protein=targets["protein"],
        target_fat=targets["fat"],
        target_carbs=targets["carbs"],

        user_id=current_user.id
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile created successfully",
        "targets": targets
    }

@app.put("/profile")
def update_profile(
    request: ProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # recalculate targets
    targets = calculate_daily_targets(
        weight=request.weight,
        height=request.height,
        age=request.age,
        sex=request.sex,
        target=request.target,
        activity_level=request.activity_level,
        exercise_level=request.exercise_level
    )

    # update profile fields
    profile.age = request.age
    profile.weight = request.weight
    profile.height = request.height

    profile.sex = request.sex
    profile.target = request.target
    profile.activity_level = request.activity_level
    profile.exercise_level = request.exercise_level

    # update targets
    profile.target_calories = targets["calories"]
    profile.target_protein = targets["protein"]
    profile.target_fat = targets["fat"]
    profile.target_carbs = targets["carbs"]

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "targets": targets
    }

@app.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "user": {
            "username": current_user.username
        },

        "profile": {
            "age": profile.age,
            "weight": profile.weight,
            "height": profile.height,

            "target": profile.target,
            "activity_level": profile.activity_level,
            "exercise_level": profile.exercise_level
        },

        "targets": {
            "calories": profile.target_calories,
            "protein": profile.target_protein,
            "fat": profile.target_fat,
            "carbs": profile.target_carbs
        }
    }

@app.get("/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    today = date.today()

    meals = db.query(Meal).filter(
        Meal.user_id == current_user.id,
        func.date(Meal.created_at) == today
    ).all()

    consumed = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0
    }

    for meal in meals:
        consumed["calories"] += meal.calories
        consumed["protein"] += meal.protein
        consumed["fat"] += meal.fat
        consumed["carbs"] += meal.carbs

    targets = {
        "calories": profile.target_calories,
        "protein": profile.target_protein,
        "fat": profile.target_fat,
        "carbs": profile.target_carbs
    }

    remaining = {
        "calories": targets["calories"] - consumed["calories"],
        "protein": targets["protein"] - consumed["protein"],
        "fat": targets["fat"] - consumed["fat"],
        "carbs": targets["carbs"] - consumed["carbs"]
    }

    percentage = {
        "calories": round((consumed["calories"] / targets["calories"]) * 100, 1),
        "protein": round((consumed["protein"] / targets["protein"]) * 100, 1),
        "fat": round((consumed["fat"] / targets["fat"]) * 100, 1),
        "carbs": round((consumed["carbs"] / targets["carbs"]) * 100, 1),
    }

    return {
        "targets": targets, 
        "consumed": consumed,
        "remaining": remaining,
        "percentage": percentage
    }


@app.get("/foods")
def get_foods(db: Session = Depends(get_db)):

    foods = db.query(Food).all()

    return foods

# --- 1. Predict food ---
@app.post("/predict")
async def predict(file: UploadFile = File(...), current_user: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    filename = f"temp_{uuid.uuid4()}.jpg"

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    CONFIDENCE_THRESHOLD = 0.6

    predictions = predict_image(filename)

    top_prediction = predictions[0]

    if top_prediction["confidence"] < CONFIDENCE_THRESHOLD:
        return {
            "success": False,
            "message": "Low confidence prediction",
            "predictions": predictions
        }

    return {
        "success": True,
        "predictions": predictions
    }

# --- 2. Log meal ---
@app.post("/meals")
def log_meal(
    request: MealRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    nutrition = calculate_nutrition(
        db,
        request.food,
        request.amount
    )

    meal = Meal(
        food=request.food,
        amount=request.amount,
        calories=nutrition["calories"],
        protein=nutrition["protein"],
        fat=nutrition["fat"],
        carbs=nutrition["carbs"],
        user_id=current_user.id
    )

    db.add(meal)
    db.commit()
    db.refresh(meal)

    return {
        "message": "Meal logged successfully"
    }

# --- 3. Daily summary ---
@app.get("/summary")
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    meals = db.query(Meal).filter(Meal.user_id == current_user.id).all()

    total = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0
    }

    for meal in meals:
        total["calories"] += meal.calories
        total["protein"] += meal.protein
        total["fat"] += meal.fat
        total["carbs"] += meal.carbs

    return total

