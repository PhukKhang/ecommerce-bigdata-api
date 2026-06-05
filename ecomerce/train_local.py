import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from pyspark.ml import Pipeline
from pyspark.ml.classification import (
    GBTClassifier,
    LogisticRegression,
    RandomForestClassifier,
)
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StandardScaler, StringIndexer, VectorAssembler
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F


FEATURE_COLUMNS = [
    "payment_type_index",
    "payment_installments",
    "number_of_items",
    "avg_item_price",
    "delivery_time",
    "delivery_delay",
    "shipping_duration",
    "order_total_value",
    "customer_total_orders",
    "customer_total_spent",
    "avg_review_score_customer",
]

DATASET_SOURCE_URL = (
    "https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train the e-commerce satisfaction models from local Olist CSV files."
    )
    parser.add_argument(
        "--dataset-dir",
        required=True,
        type=Path,
        help="Directory containing the Olist CSV files.",
    )
    parser.add_argument(
        "--model-output",
        required=True,
        type=Path,
        help="Directory where the best Spark PipelineModel will be saved.",
    )
    parser.add_argument(
        "--metrics-output",
        required=True,
        type=Path,
        help="JSON file where evaluation metrics will be written.",
    )
    return parser.parse_args()


def read_csv(spark: SparkSession, dataset_dir: Path, file_name: str) -> DataFrame:
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .option("multiLine", True)
        .option("quote", '"')
        .option("escape", '"')
        .csv(str(dataset_dir / file_name))
    )


def build_ml_dataset(spark: SparkSession, dataset_dir: Path) -> DataFrame:
    customers_df = read_csv(spark, dataset_dir, "olist_customers_dataset.csv")
    orders_df = read_csv(spark, dataset_dir, "olist_orders_dataset.csv")
    reviews_df = read_csv(spark, dataset_dir, "olist_order_reviews_dataset.csv")
    payments_df = read_csv(spark, dataset_dir, "olist_order_payments_dataset.csv")
    items_df = read_csv(spark, dataset_dir, "olist_order_items_dataset.csv")

    review_order_window = Window.partitionBy("order_id").orderBy(
        F.col("_review_answer_at").desc_nulls_last(),
        F.col("_review_creation_at").desc_nulls_last(),
        F.col("review_id").desc_nulls_last(),
    )

    reviews_order_df = (
        reviews_df.filter(F.col("order_id").isNotNull())
        .withColumn("review_score", F.col("review_score").cast("int"))
        .filter(F.col("review_score").isNotNull())
        .dropDuplicates()
        .withColumn("_review_answer_at", F.to_timestamp("review_answer_timestamp"))
        .withColumn("_review_creation_at", F.to_timestamp("review_creation_date"))
        .withColumn("_row_number", F.row_number().over(review_order_window))
        .filter(F.col("_row_number") == 1)
        .drop("_row_number", "_review_answer_at", "_review_creation_at")
    )

    payment_order_window = Window.partitionBy("order_id").orderBy(
        F.col("payment_value").desc_nulls_last(),
        F.col("payment_sequential").asc_nulls_last(),
    )

    primary_payment_df = (
        payments_df.withColumn("_row_number", F.row_number().over(payment_order_window))
        .filter(F.col("_row_number") == 1)
        .select("order_id", "payment_type", "payment_installments")
    )

    payments_agg_df = (
        payments_df.groupBy("order_id")
        .agg(F.sum("payment_value").alias("total_payment_value"))
        .join(primary_payment_df, "order_id", "left")
    )

    order_product_agg_df = items_df.groupBy("order_id").agg(
        F.count("*").alias("number_of_items"),
        F.sum("price").alias("total_product_value"),
        F.sum("freight_value").alias("total_freight_value"),
        F.avg("price").alias("avg_item_price"),
    )

    master_orders_df = (
        orders_df.join(
            customers_df.select("customer_id", "customer_unique_id"),
            "customer_id",
            "left",
        )
        .join(reviews_order_df, "order_id", "left")
        .join(payments_agg_df, "order_id", "left")
        .join(order_product_agg_df, "order_id", "left")
        .withColumn(
            "delivery_time",
            F.datediff("order_delivered_customer_date", "order_purchase_timestamp"),
        )
        .withColumn(
            "delivery_delay",
            F.datediff(
                "order_delivered_customer_date", "order_estimated_delivery_date"
            ),
        )
        .withColumn(
            "shipping_duration",
            F.datediff("order_delivered_carrier_date", "order_approved_at"),
        )
        .withColumn(
            "order_total_value",
            F.col("total_product_value") + F.col("total_freight_value"),
        )
    )

    master_rows = master_orders_df.count()
    unique_orders = master_orders_df.select("order_id").distinct().count()
    if master_rows != unique_orders:
        raise ValueError(
            f"master_orders must contain one row per order: rows={master_rows}, "
            f"unique_orders={unique_orders}"
        )

    order_history_events_df = master_orders_df.select(
        "order_id",
        "customer_unique_id",
        F.col("order_purchase_timestamp").cast("long").alias("event_time"),
        F.lit("order").alias("event_type"),
        F.lit(1).alias("order_increment"),
        F.col("order_total_value").cast("double").alias("spent_increment"),
        F.lit(None).cast("double").alias("review_score_increment"),
    )

    review_history_events_df = (
        master_orders_df.select(
            F.lit(None).cast("string").alias("order_id"),
            "customer_unique_id",
            F.to_timestamp("review_answer_timestamp").cast("long").alias("event_time"),
            F.col("order_purchase_timestamp")
            .cast("long")
            .alias("review_order_purchase_time"),
            F.lit("review").alias("event_type"),
            F.lit(0).alias("order_increment"),
            F.lit(0.0).alias("spent_increment"),
            F.col("review_score").cast("double").alias("review_score_increment"),
        )
        .filter(F.col("event_time").isNotNull())
        .filter(F.col("event_time") > F.col("review_order_purchase_time"))
        .filter(F.col("review_score_increment").isNotNull())
        .drop("review_order_purchase_time")
    )

    history_events_df = order_history_events_df.unionByName(review_history_events_df)
    customer_history_window = (
        Window.partitionBy("customer_unique_id")
        .orderBy("event_time")
        .rangeBetween(Window.unboundedPreceding, -1)
    )

    customer_history_df = (
        history_events_df.withColumn(
            "customer_total_orders",
            F.coalesce(
                F.sum("order_increment").over(customer_history_window), F.lit(0)
            ).cast("long"),
        )
        .withColumn(
            "customer_total_spent",
            F.coalesce(
                F.sum("spent_increment").over(customer_history_window), F.lit(0.0)
            ),
        )
        .withColumn(
            "avg_review_score_customer",
            F.avg("review_score_increment").over(customer_history_window),
        )
        .filter(F.col("event_type") == "order")
        .select(
            "order_id",
            "customer_total_orders",
            "customer_total_spent",
            "avg_review_score_customer",
        )
    )

    return (
        master_orders_df.join(customer_history_df, "order_id", "left")
        .filter(F.col("review_score").isNotNull())
        .withColumn(
            "label", F.when(F.col("review_score") >= 4, F.lit(1)).otherwise(F.lit(0))
        )
        .select(
            "order_id",
            "order_purchase_timestamp",
            "payment_type",
            "payment_installments",
            "number_of_items",
            "avg_item_price",
            "delivery_time",
            "delivery_delay",
            "shipping_duration",
            "order_total_value",
            "customer_total_orders",
            "customer_total_spent",
            "avg_review_score_customer",
            "label",
        )
        .fillna(
            {
                "payment_type": "unknown",
                "payment_installments": 0,
                "number_of_items": 0,
                "avg_item_price": 0.0,
                "delivery_time": 0,
                "delivery_delay": 0,
                "shipping_duration": 0,
                "order_total_value": 0.0,
                "customer_total_orders": 0,
                "customer_total_spent": 0.0,
                "avg_review_score_customer": 0.0,
            }
        )
        .dropDuplicates(["order_id"])
    )


def label_distribution(dataset: DataFrame) -> dict[str, int]:
    return {
        str(row["label"]): row["count"]
        for row in dataset.groupBy("label").count().orderBy("label").collect()
    }


def evaluate_predictions(model_name: str, predictions: DataFrame) -> dict[str, float]:
    counts = (
        predictions.agg(
            F.sum(
                F.when((F.col("label") == 1) & (F.col("prediction") == 1), 1).otherwise(
                    0
                )
            ).alias("tp"),
            F.sum(
                F.when((F.col("label") == 0) & (F.col("prediction") == 0), 1).otherwise(
                    0
                )
            ).alias("tn"),
            F.sum(
                F.when((F.col("label") == 0) & (F.col("prediction") == 1), 1).otherwise(
                    0
                )
            ).alias("fp"),
            F.sum(
                F.when((F.col("label") == 1) & (F.col("prediction") == 0), 1).otherwise(
                    0
                )
            ).alias("fn"),
        )
        .first()
        .asDict()
    )

    tp = counts["tp"]
    tn = counts["tn"]
    fp = counts["fp"]
    fn = counts["fn"]
    total = tp + tn + fp + fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    negative_recall = tn / (tn + fp) if tn + fp else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    roc_auc = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC",
    ).evaluate(predictions)
    pr_auc = BinaryClassificationEvaluator(
        labelCol="label",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderPR",
    ).evaluate(predictions)

    return {
        "model": model_name,
        "accuracy": (tp + tn) / total if total else 0.0,
        "precision": precision,
        "recall": recall,
        "negative_recall": negative_recall,
        "balanced_accuracy": (recall + negative_recall) / 2,
        "f1": f1,
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def make_pipeline(classifier) -> Pipeline:
    return Pipeline(
        stages=[
            StringIndexer(
                inputCol="payment_type",
                outputCol="payment_type_index",
                handleInvalid="keep",
            ),
            VectorAssembler(inputCols=FEATURE_COLUMNS, outputCol="features"),
            StandardScaler(
                inputCol="features",
                outputCol="scaled_features",
                withStd=True,
                withMean=False,
            ),
            classifier,
        ]
    )


def main() -> None:
    args = parse_args()
    dataset_dir = args.dataset_dir.resolve()
    model_output = args.model_output.resolve()
    metrics_output = args.metrics_output.resolve()

    spark = (
        SparkSession.builder.master("local[4]")
        .appName("EcommerceSatisfactionTraining")
        .config("spark.sql.shuffle.partitions", "16")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        ml_dataset = build_ml_dataset(spark, dataset_dir).cache()
        ml_rows = ml_dataset.count()
        unique_orders = ml_dataset.select("order_id").distinct().count()
        if ml_rows != unique_orders:
            raise ValueError(
                f"ml_dataset must contain one row per order: rows={ml_rows}, "
                f"unique_orders={unique_orders}"
            )

        dataset_with_epoch = ml_dataset.withColumn(
            "_purchase_epoch", F.col("order_purchase_timestamp").cast("long")
        )
        split_epoch = dataset_with_epoch.approxQuantile(
            "_purchase_epoch", [0.8], 0.001
        )[0]
        train_df = dataset_with_epoch.filter(F.col("_purchase_epoch") < split_epoch).cache()
        test_df = dataset_with_epoch.filter(F.col("_purchase_epoch") >= split_epoch).cache()

        train_rows = train_df.count()
        test_rows = test_df.count()
        print(f"ML rows: {ml_rows}")
        print(f"Split timestamp: {datetime.fromtimestamp(split_epoch, timezone.utc).isoformat()}")
        print(f"Train rows: {train_rows}")
        print(f"Test rows: {test_rows}")

        classifiers = {
            "Logistic Regression": LogisticRegression(
                featuresCol="scaled_features", labelCol="label"
            ),
            "Random Forest": RandomForestClassifier(
                featuresCol="scaled_features",
                labelCol="label",
                numTrees=100,
                seed=42,
            ),
            "GBTClassifier": GBTClassifier(
                featuresCol="scaled_features",
                labelCol="label",
                maxIter=20,
                seed=42,
            ),
        }

        trained_models = {}
        model_metrics = []
        for model_name, classifier in classifiers.items():
            print(f"Training: {model_name}")
            model = make_pipeline(classifier).fit(train_df)
            predictions = model.transform(test_df).cache()
            metrics = evaluate_predictions(model_name, predictions)
            print(json.dumps(metrics, indent=2))
            trained_models[model_name] = model
            model_metrics.append(metrics)
            predictions.unpersist()

        best_metrics = max(
            model_metrics,
            key=lambda metrics: (metrics["balanced_accuracy"], metrics["roc_auc"]),
        )
        best_model_name = best_metrics["model"]
        print(f"Best model: {best_model_name}")

        metrics_payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dataset_source": str(dataset_dir),
            "dataset_source_url": DATASET_SOURCE_URL,
            "ml_rows": ml_rows,
            "split_timestamp": datetime.fromtimestamp(split_epoch, timezone.utc).isoformat(),
            "train_rows": train_rows,
            "test_rows": test_rows,
            "train_label_distribution": label_distribution(train_df),
            "test_label_distribution": label_distribution(test_df),
            "selection_metric": "balanced_accuracy",
            "best_model": best_model_name,
            "models": model_metrics,
        }
        metrics_output.parent.mkdir(parents=True, exist_ok=True)
        metrics_output.write_text(
            json.dumps(metrics_payload, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Metrics saved: {metrics_output}")

        model_output.parent.mkdir(parents=True, exist_ok=True)
        trained_models[best_model_name].write().overwrite().save(str(model_output))
        print(f"Model saved: {model_output}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
