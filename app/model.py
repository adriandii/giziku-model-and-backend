import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = load_model("model/mobilenet_food_model.h5", compile=False)

class_names = [
    "ayam_goreng","ayam_pop","bubur_ayam","rendang","dendeng",
    "ketoprak","mie_ayam","pecel_lele","rawon","sate_ayam",
    "soto_ayam","tahu_goreng","telur_balado","telur_dadar","tempe_goreng"
]

def predict_image(img_file):
    img = image.load_img(img_file, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    
    top_indices = preds[0].argsort()[-3:][::-1]

    results = []

    for idx in top_indices:
        results.append({
            "food": class_names[idx],
            "confidence": float(preds[0][idx])
        })

    return results