from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    payment_type: str = Field(examples=["credit_card"])
    payment_installments: int = Field(examples=[1])
    number_of_items: int = Field(examples=[1])
    avg_item_price: float = Field(examples=[100.0])
    delivery_time: int = Field(examples=[7])
    delivery_delay: int = Field(examples=[-2])
    shipping_duration: int = Field(examples=[1])
    order_total_value: float = Field(examples=[110.0])
    customer_total_orders: int = Field(examples=[0])
    customer_total_spent: float = Field(examples=[0.0])
    avg_review_score_customer: float = Field(examples=[0.0])


class PredictionResponse(BaseModel):
    prediction: str
    predicted_label: int
    probabilities: dict[str, float]
    confidence: str
    confidence_score: float
    model: str


class HealthResponse(BaseModel):
    status: str
    service: str
    model: str
    model_path: str
    model_artifact_found: bool
