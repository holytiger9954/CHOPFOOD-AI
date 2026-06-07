import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "inspection_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_inspection(data):

    df = pd.DataFrame([{
        "INSPECTION_TYPE": data.inspection_type,
        "TARGET_TYPE": data.target_type,
        "INSPECTION_MONTH": data.inspection_month,
        "INSPECTION_WEEKDAY": data.inspection_weekday
    }])

    pred = model.predict(df)[0]

    probs = model.predict_proba(df)[0]
    classes = model.classes_

    prob_map = dict(zip(classes, probs))

    return {
        "risk_level": pred,
        "normal_prob": round(prob_map.get("NORMAL", 0) * 100, 2),
        "warning_prob": round(prob_map.get("WARNING", 0) * 100, 2),
        "risk_prob": round(prob_map.get("RISK", 0) * 100, 2)
    }