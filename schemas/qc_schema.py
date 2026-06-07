from pydantic import BaseModel


class QcPredictRequest(BaseModel):
    lot_qty: float
    qc_qty: float
    item_type: int
    item_qc_type: int
    qc_type: int
    work_order_qty: float
    qc_month: int
    qc_weekday: int
    inspection_risk_score: int
    summer_flag: int
    winter_flag: int


class QcPredictResponse(BaseModel):
    risk_level: str
    low_prob: float
    medium_prob: float
    high_prob: float