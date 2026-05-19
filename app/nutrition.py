from app.models import Food

def calculate_nutrition(db, food_name, amount):

    food = db.query(Food).filter(
        Food.name == food_name
    ).first()

    if not food:
        return None
    
    if food.serving_type == "gram":

        multiplier = amount / 100

    else:
        multiplier = amount

    return {
        "calories": round(food.calories * multiplier, 2),
        "protein": round(food.protein * multiplier, 2),
        "fat": round(food.fat * multiplier, 2),
        "carbs": round(food.carbs * multiplier, 2)
    }