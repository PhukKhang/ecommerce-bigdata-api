import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DATASET_SOURCE_URL = (
    "https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build dashboard JSON and Power BI CSV files from Olist CSV data."
    )
    parser.add_argument("--dataset-dir", required=True, type=Path)
    parser.add_argument("--metrics", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def read_csv(dataset_dir: Path, file_name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(dataset_dir / file_name, low_memory=False, **kwargs)


def round_records(frame: pd.DataFrame, digits: int = 2) -> list[dict]:
    rounded = frame.copy()
    numeric_columns = rounded.select_dtypes(include="number").columns
    rounded[numeric_columns] = rounded[numeric_columns].round(digits)
    return rounded.to_dict(orient="records")


def write_csv(frame: pd.DataFrame, output_dir: Path, name: str) -> None:
    frame.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8-sig")


def build_dashboard_data(
    dataset_dir: Path, metrics_path: Path, output_dir: Path
) -> dict:
    orders = read_csv(
        dataset_dir,
        "olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    customers = read_csv(dataset_dir, "olist_customers_dataset.csv")
    sellers = read_csv(dataset_dir, "olist_sellers_dataset.csv")
    items = read_csv(dataset_dir, "olist_order_items_dataset.csv")
    products = read_csv(dataset_dir, "olist_products_dataset.csv")
    translations = read_csv(dataset_dir, "product_category_name_translation.csv")
    payments = read_csv(dataset_dir, "olist_order_payments_dataset.csv")
    reviews = read_csv(
        dataset_dir,
        "olist_order_reviews_dataset.csv",
        parse_dates=["review_creation_date", "review_answer_timestamp"],
    )

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

    order_payments = (
        payments.groupby("order_id", as_index=False)["payment_value"]
        .sum()
        .rename(columns={"payment_value": "revenue"})
    )
    orders_sales = orders.merge(order_payments, on="order_id", how="left")
    orders_sales["revenue"] = orders_sales["revenue"].fillna(0.0)
    orders_sales["month"] = (
        orders_sales["order_purchase_timestamp"].dt.to_period("M").astype(str)
    )

    monthly_revenue = (
        orders_sales.groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .sort_values("month")
    )

    product_items = (
        items.merge(
            products[["product_id", "product_category_name"]],
            on="product_id",
            how="left",
        )
        .merge(translations, on="product_category_name", how="left")
        .merge(sellers[["seller_id", "seller_state"]], on="seller_id", how="left")
    )
    product_items["category"] = product_items[
        "product_category_name_english"
    ].fillna(product_items["product_category_name"].fillna("unknown"))
    product_items["item_revenue"] = (
        product_items["price"].fillna(0.0) + product_items["freight_value"].fillna(0.0)
    )

    top_categories = (
        product_items.groupby("category", as_index=False)
        .agg(revenue=("item_revenue", "sum"), items=("product_id", "count"))
        .sort_values("revenue", ascending=False)
        .head(10)
    )
    top_sellers = (
        product_items.groupby(["seller_id", "seller_state"], as_index=False)
        .agg(revenue=("item_revenue", "sum"), items=("product_id", "count"))
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    payment_methods = (
        payments.groupby("payment_type", as_index=False)
        .agg(
            revenue=("payment_value", "sum"),
            transactions=("payment_type", "size"),
            orders=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )

    latest_reviews = (
        reviews.sort_values(
            ["order_id", "review_answer_timestamp", "review_creation_date", "review_id"]
        )
        .drop_duplicates("order_id", keep="last")
        .copy()
    )
    latest_reviews["review_score"] = latest_reviews["review_score"].astype(int)
    review_distribution = (
        latest_reviews.groupby("review_score", as_index=False)
        .size()
        .rename(columns={"size": "reviews"})
        .sort_values("review_score")
    )

    delivered = orders.dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date"]
    ).copy()
    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    delivered["delay_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    delivered["delivery_status"] = delivered["delay_days"].apply(
        lambda days: "late" if days > 0 else "on_time_or_early"
    )
    delivery_summary = (
        delivered.groupby("delivery_status", as_index=False)
        .agg(orders=("order_id", "nunique"))
        .sort_values("delivery_status")
    )

    state_sales = (
        orders_sales.merge(
            customers[["customer_id", "customer_state"]], on="customer_id", how="left"
        )
        .groupby("customer_state", as_index=False)
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    total_revenue = float(order_payments["revenue"].sum())
    total_orders = int(orders["order_id"].nunique())
    late_orders = int((delivered["delay_days"] > 0).sum())
    delivery_orders = int(delivered["order_id"].nunique())
    positive_reviews = int((latest_reviews["review_score"] >= 4).sum())
    total_reviews = int(len(latest_reviews))

    powerbi_dir = output_dir / "powerbi"
    powerbi_dir.mkdir(parents=True, exist_ok=True)
    write_csv(monthly_revenue, powerbi_dir, "monthly_revenue")
    write_csv(top_categories, powerbi_dir, "top_categories")
    write_csv(top_sellers, powerbi_dir, "top_sellers")
    write_csv(payment_methods, powerbi_dir, "payment_methods")
    write_csv(review_distribution, powerbi_dir, "review_distribution")
    write_csv(delivery_summary, powerbi_dir, "delivery_summary")
    write_csv(state_sales, powerbi_dir, "state_sales")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_source_url": DATASET_SOURCE_URL,
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "unique_customers": int(customers["customer_unique_id"].nunique()),
            "sellers": int(sellers["seller_id"].nunique()),
            "average_order_value": round(total_revenue / total_orders, 2),
            "average_review_score": round(float(latest_reviews["review_score"].mean()), 2),
            "positive_review_rate": round(positive_reviews / total_reviews, 4),
            "late_delivery_rate": round(late_orders / delivery_orders, 4),
        },
        "delivery": {
            "delivered_orders": delivery_orders,
            "late_orders": late_orders,
            "on_time_or_early_orders": delivery_orders - late_orders,
            "average_delivery_days": round(float(delivered["delivery_days"].mean()), 2),
            "average_delay_days": round(float(delivered["delay_days"].mean()), 2),
        },
        "monthly_revenue": round_records(monthly_revenue),
        "top_categories": round_records(top_categories),
        "top_sellers": round_records(top_sellers),
        "payment_methods": round_records(payment_methods),
        "review_distribution": round_records(review_distribution),
        "state_sales": round_records(state_sales),
        "ml": metrics,
    }


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    payload = build_dashboard_data(
        args.dataset_dir.resolve(), args.metrics.resolve(), output_dir
    )
    output_path = data_dir / "dashboard_data.json"
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Dashboard data saved: {output_path}")


if __name__ == "__main__":
    main()
