from pydantic import BaseModel


class InspectionPredictRequest(BaseModel):
    inspection_type: str
    target_type: str
    inspection_month: int
    inspection_weekday: int


class InspectionPredictResponse(BaseModel):
    risk_level: str
    normal_prob: float
    warning_prob: float
    risk_prob: float