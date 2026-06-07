from fastapi import FastAPI

from schemas.qc_schema import QcPredictRequest, QcPredictResponse
from schemas.work_schema import WorkPredictRequest
from schemas.inspection_schema import InspectionPredictRequest
from schemas.io_schema import IoPredictRequest

from services.qc_predict_service import predict_qc
from services.work_predict_service import predict_work
from services.inspection_predict_service import predict_inspection
from services.io_predict_service import predict_io


app = FastAPI(
    title="ChopChop AI API",
    description="MES AI prediction API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "ChopChop AI server is running"
    }


@app.post("/predict/qc", response_model=QcPredictResponse)
def predict_qc_api(request: QcPredictRequest):
    return predict_qc(request)

@app.post("/predict/work")
def predict_work_api(request: WorkPredictRequest):
    return predict_work(request)

@app.post("/predict/inspection")
def predict_inspection_api(request: InspectionPredictRequest):
    return predict_inspection(request)

@app.post("/predict/io")
def predict_io_api(request: IoPredictRequest):
    return predict_io(request)