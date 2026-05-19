from app.database import Base, SessionLocal, engine
from app.models import Food


FOOD_SEED_DATA = [
    {"name": "ayam goreng", "calories": 250, "protein": 28, "fat": 12, "carbs": 0.3, "serving_type": "gram"},
    {"name": "ayam pop", "calories": 170, "protein": 20, "fat": 9, "carbs": 5, "serving_type": "gram"},
    {"name": "bubur ayam", "calories": 372, "protein": 22, "fat": 12, "carbs": 36, "serving_type": "portion"},
    {"name": "daging rendang", "calories": 194, "protein": 23, "fat": 8, "carbs": 8, "serving_type": "gram"},
    {"name": "dendeng balado", "calories": 123, "protein": 10, "fat": 8, "carbs": 3, "serving_type": "piece"},
    {"name": "ketoprak", "calories": 420, "protein": 16, "fat": 15, "carbs": 50, "serving_type": "portion"},
    {"name": "mie ayam", "calories": 415, "protein": 17, "fat": 19, "carbs": 46, "serving_type": "portion"},
    {"name": "pecel lele", "calories": 292, "protein": 23, "fat": 17, "carbs": 12, "serving_type": "portion"},
    {"name": "rawon", "calories": 288, "protein": 23, "fat": 18, "carbs": 8, "serving_type": "portion"},
    {"name": "sate ayam", "calories": 34, "protein": 3, "fat": 3, "carbs": 1, "serving_type": "skewer"},
    {"name": "soto ayam", "calories": 312, "protein": 24, "fat": 15, "carbs": 20, "serving_type": "portion"},
    {"name": "tahu goreng", "calories": 35, "protein": 2, "fat": 3, "carbs": 1, "serving_type": "piece"},
    {"name": "telur balado", "calories": 71, "protein": 6, "fat": 5, "carbs": 1, "serving_type": "piece"},
    {"name": "telur dadar", "calories": 153, "protein": 11, "fat": 12, "carbs": 1, "serving_type": "gram"},
    {"name": "tempe goreng", "calories": 34, "protein": 2, "fat": 2.5, "carbs": 2, "serving_type": "piece"},
    {"name": "nasi putih", "calories": 129, "protein": 3, "fat": 0.2, "carbs": 28, "serving_type": "gram"},
]


def seed_foods() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_names = {
            row[0]
            for row in db.query(Food.name).all()
        }

        to_insert = [
            Food(**item)
            for item in FOOD_SEED_DATA
            if item["name"] not in existing_names
        ]

        if to_insert:
            db.add_all(to_insert)
            db.commit()
            print(f"Inserted {len(to_insert)} food rows.")
        else:
            print("No new rows inserted. Seed data already exists.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_foods()
