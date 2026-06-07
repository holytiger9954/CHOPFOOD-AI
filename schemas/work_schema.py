from pydantic import BaseModel


class WorkPredictRequest(BaseModel):
    work_order_qty: float
    work_prev_qty: float
    work_status: int
    plan_fin_qty: float
    plan_wp_qty: float
    item_type: int
    work_month: int
    work_weekday: int
    summer_flag: int
    winter_flag: int
    qty_risk_score: int
    season_risk_score: int


class WorkPredictResponse(BaseModel):
    risk_level: str
    normal_prob: float
    delay_prob: float
    risk_prob: float