from fastapi import FastAPI, HTTPException

from app.schema import HealthResponse, PredictionRequest, PredictionResponse
from app.predictor import get_health, predict

app = FastAPI(
    title="E-commerce Review Prediction API",
    version="1.0.0",
    description="FastAPI service for Random Forest customer review prediction."
)


@app.get("/", response_model=HealthResponse)
def home():
    return get_health()


@app.get("/health", response_model=HealthResponse)
def health_check():
    return get_health()


@app.post("/predict", response_model=PredictionResponse)
def predict_review(
    request: PredictionRequest
):
    try:
        return predict(request)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Prediction service is unavailable: {exc}"
        ) from exc
