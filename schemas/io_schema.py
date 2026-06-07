from pydantic import BaseModel


class IoPredictRequest(BaseModel):
    io_qty: float
    lot_qty: float
    lot_fqty: float
    item_type: int
    item_unit_price: float
    io_month: int
    io_weekday: int


class IoPredictResponse(BaseModel):
    risk_level: str
    low_prob: float
    warning_prob: float
    high_prob: float