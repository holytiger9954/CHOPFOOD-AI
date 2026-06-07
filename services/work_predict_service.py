import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "work_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_work(data):

    df = pd.DataFrame([{
        "WORK_ORDER_QTY": data.work_order_qty,
        "WORK_PREV_QTY": data.work_prev_qty,
        "WORK_STATUS": data.work_status,
        "PLAN_FIN_QTY": data.plan_fin_qty,
        "PLAN_WP_QTY": data.plan_wp_qty,
        "ITEM_TYPE": data.item_type,
        "WORK_MONTH": data.work_month,
        "WORK_WEEKDAY": data.work_weekday,
        "SUMMER_FLAG": data.summer_flag,
        "WINTER_FLAG": data.winter_flag,
        "QTY_RISK_SCORE": data.qty_risk_score,
        "SEASON_RISK_SCORE": data.season_risk_score
    }])

    pred = model.predict(df)[0]

    probs = model.predict_proba(df)[0]
    classes = model.classes_

    prob_map = dict(zip(classes, probs))

    return {
        "risk_level": pred,
        "normal_prob": round(prob_map.get("NORMAL", 0) * 100, 2),
        "delay_prob": round(prob_map.get("DELAY", 0) * 100, 2),
        "risk_prob": round(prob_map.get("RISK", 0) * 100, 2)
    }