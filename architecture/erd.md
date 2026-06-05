# Olist E-commerce ERD

ERD ben duoi mo ta cac bang raw va quan he chinh duoc dung trong ETL.

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDERS ||--o{ PAYMENTS : paid_by
    ORDERS ||--o{ REVIEWS : receives
    PRODUCTS ||--o{ ORDER_ITEMS : appears_in
    SELLERS ||--o{ ORDER_ITEMS : fulfills
    CATEGORY_TRANSLATION ||--o{ PRODUCTS : translates

    CUSTOMERS {
        string customer_id PK
        string customer_unique_id
        int customer_zip_code_prefix
        string customer_city
        string customer_state
    }

    ORDERS {
        string order_id PK
        string customer_id FK
        string order_status
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }

    ORDER_ITEMS {
        string order_id FK
        int order_item_id
        string product_id FK
        string seller_id FK
        timestamp shipping_limit_date
        double price
        double freight_value
    }

    PAYMENTS {
        string order_id FK
        int payment_sequential
        string payment_type
        int payment_installments
        double payment_value
    }

    REVIEWS {
        string review_id
        string order_id FK
        int review_score
        string review_comment_title
        string review_comment_message
        timestamp review_creation_date
        timestamp review_answer_timestamp
    }

    PRODUCTS {
        string product_id PK
        string product_category_name FK
        int product_weight_g
        int product_length_cm
        int product_height_cm
        int product_width_cm
    }

    SELLERS {
        string seller_id PK
        int seller_zip_code_prefix
        string seller_city
        string seller_state
    }

    CATEGORY_TRANSLATION {
        string product_category_name PK
        string product_category_name_english
    }
```

## Grain Cua Silver Layer

`reviews` khong the join truc tiep vao `orders`: mot `order_id` co the co nhieu
review record. Notebook ETL xep hang review theo `review_answer_timestamp`,
`review_creation_date`, `review_id` va giu review moi nhat:

```mermaid
flowchart LR
    A["Raw reviews"] --> B["Filter valid order_id and review_score"]
    B --> C["Rank review rows inside each order_id"]
    C --> D["Silver reviews_order: one row per order_id"]
    E["Orders"] --> F["Silver master_orders"]
    D --> F
    G["Aggregated payments"] --> F
    H["Aggregated order items"] --> F
```

## Gold Feature Layer

Feature lich su customer chi su dung su kien co timestamp nho hon
`order_purchase_timestamp` cua order hien tai:

```mermaid
flowchart LR
    A["Order events"] --> C["Customer event timeline"]
    B["Review answer events"] --> C
    C --> D["Window: event_time < current purchase time"]
    D --> E["customer_total_orders"]
    D --> F["customer_total_spent"]
    D --> G["avg_review_score_customer"]
```
