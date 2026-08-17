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
    {"name": "ayam bakar", "calories": 200, "protein": 28, "fat": 10, "carbs": 0.3, "serving_type": "gram"},
    {"name": "ayam betutu", "calories": 212, "protein": 15, "fat": 17, "carbs": 3, "serving_type": "gram"},
    {"name": "perkedel kentang", "calories": 143, "protein": 3, "fat": 7, "carbs": 17, "serving_type": "gram"},
    {"name": "ikan goreng", "calories": 170, "protein": 25, "fat": 3, "carbs": 0, "serving_type": "gram"},
    {"name": "ikan bakar", "calories": 150, "protein": 25, "fat": 3, "carbs": 1, "serving_type": "gram"},
    {"name": "tempe mendoan", "calories": 200, "protein": 11, "fat": 13, "carbs": 13, "serving_type": "gram"},
    {"name": "pempek", "calories": 234, "protein": 15, "fat": 6, "carbs": 28, "serving_type": "portion"},
    {"name": "sate padang", "calories": 24, "protein": 3, "fat": 1, "carbs": 1, "serving_type": "skewer"},
    {"name": "sate lilit", "calories": 51, "protein": 4, "fat": 4, "carbs": 1, "serving_type": "skewer"},
    {"name": "mie aceh", "calories": 238, "protein": 7, "fat": 7, "carbs": 37, "serving_type": "portion"},
    {"name": "soto betawi", "calories": 363, "protein": 11, "fat": 24, "carbs": 31, "serving_type": "portion"},
    {"name": "coto makassar", "calories": 289, "protein": 25, "fat": 15, "carbs": 13, "serving_type": "portion"},
    {"name": "tinutuan", "calories": 349, "protein": 11, "fat": 8, "carbs": 62, "serving_type": "portion"},
    {"name": "papeda", "calories": 58, "protein": 0, "fat": 0, "carbs": 14, "serving_type": "gram"},
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
