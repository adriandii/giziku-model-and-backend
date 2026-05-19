def calculate_daily_targets(
    sex,
    weight,
    height,
    age,
    target,
    activity_level,
    exercise_level
):

    # --- BMR (Mifflin St Jeor approximation)
    sex = sex.lower()

    if sex == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    elif sex == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    else:
        raise ValueError("sex must be either 'male' or 'female'")

    # --- activity multiplier
    activity_map = {
        "low": 1.2,
        "moderate": 1.4,
        "high": 1.6
    }

    exercise_map = {
        "never" : 0.8,
        "low": 1.0,
        "moderate": 1.2,
        "high": 1.3
    }

    calories = bmr * activity_map[activity_level] * exercise_map[exercise_level]

    # --- target adjustment
    if target == "weight_loss":
        calories -= 300

    elif target == "build_muscle":
        calories += 250

    # maintain = no change

    # --- macros
    if target == "weight_loss":
        protein = weight * 2

    elif target == "build_muscle":
        protein = weight * 1.8

    elif target == "maintain":
        protein = weight * 1.5

    fat = calories * 0.25 / 9

    carbs = (calories - (protein * 4) - (fat * 9)) / 4

    return {
        "calories": round(calories, 2),
        "protein": round(protein, 2),
        "fat": round(fat, 2),
        "carbs": round(carbs, 2)
    }