from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    meals = relationship("Meal", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    sex = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)

    activity_level = Column(String(50), nullable=False)
    exercise_level = Column(String(50), nullable=False)
    target = Column(String(50), nullable=False)

    target_calories = Column(Float, nullable=False)
    target_protein = Column(Float, nullable=False)
    target_fat = Column(Float, nullable=False)
    target_carbs = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)

    food = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="meals")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), unique=True, nullable=False)

    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)

    serving_type = Column(String(50), nullable=False)