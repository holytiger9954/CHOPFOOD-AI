import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "qc_model.pkl")

model = joblib.load(MODEL_PATH)


def predict_qc(data):
    df = pd.DataFrame([{
        "LOT_QTY": data.lot_qty,
        "QC_QTY": data.qc_qty,
        "ITEM_TYPE": data.item_type,
        "ITEM_QC_TYPE": data.item_qc_type,
        "QC_TYPE": data.qc_type,
        "WORK_ORDER_QTY": data.work_order_qty,
        "WORK_WORKER": "NONE",
        "QC_MONTH": data.qc_month,
        "QC_WEEKDAY": data.qc_weekday,
        "INSPECTION_RISK_SCORE": data.inspection_risk_score,
        "SUMMER_FLAG": data.summer_flag,
        "WINTER_FLAG": data.winter_flag
    }])

    pred = model.predict(df)[0]

    probs = model.predict_proba(df)[0]
    classes = model.classes_

    prob_map = dict(zip(classes, probs))

    return {
        "risk_level": pred,
        "low_prob": round(prob_map.get("LOW", 0) * 100, 2),
        "medium_prob": round(prob_map.get("MEDIUM", 0) * 100, 2),
        "high_prob": round(prob_map.get("HIGH", 0) * 100, 2)
    }