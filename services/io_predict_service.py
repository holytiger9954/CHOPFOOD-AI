import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "io_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_io(data):

    df = pd.DataFrame([{
        "IO_QTY": data.io_qty,
        "LOT_QTY": data.lot_qty,
        "LOT_FQTY": data.lot_fqty,
        "ITEM_TYPE": data.item_type,
        "ITEM_UNIT_PRICE": data.item_unit_price,
        "IO_MONTH": data.io_month,
        "IO_WEEKDAY": data.io_weekday
    }])

    pred = model.predict(df)[0]

    probs = model.predict_proba(df)[0]
    classes = model.classes_

    prob_map = dict(zip(classes, probs))

    return {
        "risk_level": pred,
        "low_prob": round(prob_map.get("LOW", 0) * 100, 2),
        "warning_prob": round(prob_map.get("WARNING", 0) * 100, 2),
        "high_prob": round(prob_map.get("HIGH", 0) * 100, 2)
    }