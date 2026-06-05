import os
from functools import lru_cache
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.ml.pipeline import PipelineModel

MODEL_NAME = "Random Forest"
SERVICE_NAME = "E-commerce Review Prediction API"
DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "best_model"
MODEL_PATH = Path(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)).expanduser().resolve()


@lru_cache(maxsize=1)
def get_spark():
    return (
        SparkSession.builder
        .master(os.getenv("SPARK_MASTER", "local[1]"))
        .appName("EcommercePredictionAPI")
        .config("spark.driver.host", os.getenv("SPARK_DRIVER_HOST", "127.0.0.1"))
        .config(
            "spark.driver.bindAddress",
            os.getenv("SPARK_DRIVER_BIND_ADDRESS", "127.0.0.1"),
        )
        .config("spark.ui.enabled", "false")
        .config("spark.default.parallelism", "1")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.python.worker.reuse", "true")
        .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "384m"))
        .config("spark.executor.memory", os.getenv("SPARK_EXECUTOR_MEMORY", "384m"))
        .config("spark.local.dir", os.getenv("SPARK_LOCAL_DIRS", "/tmp"))
        .getOrCreate()
    )


@lru_cache(maxsize=1)
def get_model():
    return PipelineModel.load(str(MODEL_PATH))


def get_health():
    model_artifact_found = MODEL_PATH.exists()

    return {
        "status": "ok" if model_artifact_found else "model_missing",
        "service": SERVICE_NAME,
        "model": MODEL_NAME,
        "model_path": str(MODEL_PATH),
        "model_artifact_found": model_artifact_found,
    }


def confidence_label(score):
    if score >= 0.75:
        return "high"
    if score >= 0.6:
        return "medium"
    return "low"


def predict(data):
    spark = get_spark()
    model = get_model()

    input_df = spark.range(1).select(
        lit(data.payment_type).alias("payment_type"),
        lit(data.payment_installments).cast("int").alias("payment_installments"),
        lit(data.number_of_items).cast("long").alias("number_of_items"),
        lit(data.avg_item_price).cast("double").alias("avg_item_price"),
        lit(data.delivery_time).cast("int").alias("delivery_time"),
        lit(data.delivery_delay).cast("int").alias("delivery_delay"),
        lit(data.shipping_duration).cast("int").alias("shipping_duration"),
        lit(data.order_total_value).cast("double").alias("order_total_value"),
        lit(data.customer_total_orders).cast("long").alias("customer_total_orders"),
        lit(data.customer_total_spent).cast("double").alias("customer_total_spent"),
        lit(data.avg_review_score_customer)
        .cast("double")
        .alias("avg_review_score_customer")
    )

    prediction = model.transform(input_df)

    result = prediction.select(
        "prediction",
        "probability"
    ).collect()[0]

    predicted_label = int(result["prediction"])
    probabilities = [float(value) for value in result["probability"]]
    negative_probability = probabilities[0]
    positive_probability = probabilities[1]
    confidence_score = max(probabilities)

    label = (
        "positive_review"
        if predicted_label == 1
        else "negative_review"
    )

    return {
        "prediction": label,
        "predicted_label": predicted_label,
        "probabilities": {
            "negative_review": round(negative_probability, 6),
            "positive_review": round(positive_probability, 6),
        },
        "confidence": confidence_label(confidence_score),
        "confidence_score": round(confidence_score, 6),
        "model": MODEL_NAME,
    }
