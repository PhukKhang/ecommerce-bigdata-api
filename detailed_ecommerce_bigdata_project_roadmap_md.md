# E-commerce Big Data Project
## Olist Brazilian E-commerce Dataset

---

# 1. GIỚI THIỆU DỰ ÁN

## 1.1 Mô tả bài toán

Trong lĩnh vực E-commerce, hành vi khách hàng ảnh hưởng trực tiếp đến:

- doanh thu
- mức độ hài lòng
- khả năng quay lại mua hàng
- chất lượng dịch vụ
- hiệu suất vận hành

Dataset Olist Brazilian E-commerce chứa toàn bộ dữ liệu giao dịch của một hệ thống thương mại điện tử tại Brazil, bao gồm:

- đơn hàng
- khách hàng
- sản phẩm
- seller
- thanh toán
- review
- vận chuyển

Mục tiêu của project là xây dựng một hệ thống Big Data hoàn chỉnh có khả năng:

1. xử lý dữ liệu lớn bằng PySpark
2. xây dựng ETL Pipeline
3. tạo Feature Engineering cho Machine Learning
4. train model dự đoán customer satisfaction
5. deploy model dưới dạng API
6. trực quan hóa dữ liệu bằng dashboard
7. triển khai theo hướng production-like architecture

---

# 2. MỤC TIÊU DỰ ÁN

## 2.1 Mục tiêu tổng quát

Xây dựng hệ thống phân tích và dự đoán hành vi khách hàng E-commerce sử dụng:

- Databricks
- PySpark
- Delta Lake
- Machine Learning
- FastAPI
- Docker
- Power BI

---

## 2.2 Mục tiêu kỹ thuật

### Data Engineering

- xử lý dữ liệu lớn bằng Spark
- xây dựng Bronze/Silver Layer
- tối ưu ETL Pipeline

### Machine Learning

- tạo feature dataset
- train classification model
- đánh giá model bằng nhiều metric

### Backend Engineering

- triển khai Prediction API
- realtime inference

### Visualization

- xây dựng dashboard phân tích
- trực quan hóa dữ liệu kinh doanh

---

# 3. CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ |
|---|---|
| Big Data Processing | PySpark |
| Cloud Notebook | Databricks |
| Data Storage | Delta Lake |
| Machine Learning | Spark MLlib |
| API | FastAPI |
| Container | Docker |
| Dashboard | Power BI |
| Deployment | Render / Railway |

---

# 4. KIẾN TRÚC TỔNG THỂ

## 4.1 Data Flow

```text
RAW CSV
↓
Bronze Layer
↓
Silver Layer
↓
Feature Engineering
↓
Machine Learning
↓
Saved Model
↓
FastAPI Service
↓
Dashboard / Client
```

---

## 4.2 Ý nghĩa từng layer

### RAW Layer

Chứa file CSV gốc từ Kaggle.

Mục tiêu:

- lưu dữ liệu ban đầu
- backup dữ liệu gốc
- tránh mất dữ liệu

---

### Bronze Layer

Chứa dữ liệu raw dưới dạng Delta Table.

Mục tiêu:

- tăng tốc đọc ghi
- hỗ trợ versioning
- hỗ trợ ETL

---

### Silver Layer

Chứa dữ liệu đã:

- clean
- remove duplicate
- convert datatype
- join bảng

Đây là layer dùng cho analytics và ML.

---

### Feature Layer

Tạo các feature phục vụ Machine Learning.

Ví dụ:

- delivery_delay
- order_total_value
- customer_total_orders

---

### ML Layer

Train và evaluate model.

---

### API Layer

Deploy model thành prediction service.

---

# 5. CẤU TRÚC PROJECT

```text
project/
│
├── notebooks/
│   ├── 01_data_understanding
│   ├── 02_etl_pipeline
│   ├── 03_feature_engineering
│   └── 04_machine_learning
│
├── api/
│
├── models/
│
├── dashboards/
│
├── architecture/
│
├── docs/
│
└── docker/
```

---

# 6. DAY 1 — DATA UNDERSTANDING

# Notebook: 01_data_understanding

---

## 6.1 Mục tiêu

Hiểu toàn bộ dataset trước khi xử lý.

Đây là bước quan trọng nhất trước ETL.

Nếu không hiểu dữ liệu:

- ETL sẽ sai
- feature sẽ sai
- model sẽ sai

---

## 6.2 Đọc dữ liệu CSV

### Mục tiêu

Load toàn bộ dataset vào Spark DataFrame.

### Các bảng chính

| Table | Ý nghĩa |
|---|---|
| customers | thông tin khách hàng |
| orders | thông tin đơn hàng |
| order_items | chi tiết sản phẩm trong đơn |
| payments | thông tin thanh toán |
| reviews | đánh giá khách hàng |
| sellers | thông tin seller |
| products | thông tin sản phẩm |
| category_translation | dịch category |

---

## 6.3 Kiểm tra Schema

### Mục tiêu

Hiểu datatype của từng cột.

Ví dụ:

- string
- integer
- double
- timestamp

### Ý nghĩa

Schema giúp:

- xác định kiểu dữ liệu
- tránh lỗi ETL
- hỗ trợ ML pipeline

---

## 6.4 Data Preview

### Mục tiêu

Xem dữ liệu thực tế.

### Công việc

- display dataframe
- xem sample rows
- hiểu business meaning

---

## 6.5 Kiểm tra NULL

### Mục tiêu

Xác định dữ liệu thiếu.

### Kết quả thực tế

Ví dụ:

```text
review_comment_title NULL = rất nhiều
```

Điều này hợp lý vì nhiều người dùng không viết title.

---

## 6.6 Kiểm tra Duplicate

### Mục tiêu

Đảm bảo tính toàn vẹn dữ liệu.

### Kết quả quan trọng

```text
review_id bị duplicate
```

Điều này cho thấy:

- review_id không unique
- không thể dùng làm primary key

---

## 6.7 Xác định Relationship

Ví dụ:

```text
customers.customer_id
→ orders.customer_id
```

### Ý nghĩa

Relationship dùng để:

- join bảng
- xây dựng ETL
- tạo master dataset

---

## 6.8 Thiết kế ERD

### Mục tiêu

Mô tả quan hệ giữa các bảng.

### Ý nghĩa

ERD giúp:

- hiểu kiến trúc dữ liệu
- hỗ trợ SQL
- hỗ trợ ETL pipeline

---

# 7. DAY 2 — ETL PIPELINE

# Notebook: 02_etl_pipeline

---

## 7.1 Mục tiêu

Xây dựng hệ thống ETL bằng PySpark.

---

# 7.2 Bronze Layer

## Mục tiêu

Lưu raw data dưới dạng Delta.

---

## Ý nghĩa

Delta Lake hỗ trợ:

- transaction
- versioning
- scalable storage
- fast query

---

## Các bước thực hiện

### Bước 1 — Read CSV

Đọc dữ liệu bằng Spark.

---

### Bước 2 — Save Delta

Lưu vào:

```text
bronze/customers
bronze/orders
...
```

---

# 7.3 Silver Layer

## Mục tiêu

Tạo cleaned dataset.

---

## 7.4 Handle NULL

### Công việc

- fillna
- dropna
- giữ lại NULL hợp lý

### Ví dụ

```text
review_comment_message NULL
```

Có thể giữ lại vì user không comment.

---

## 7.5 Remove Duplicate

### Công việc

```python
.dropDuplicates()
```

### Ý nghĩa

- tránh bias model
- tránh duplicate transaction

---

## 7.6 Convert Datatype

### Ví dụ

```python
to_timestamp()
```

### Mục tiêu

Convert:

- string → timestamp
- string → numeric

---

## 7.7 Join Tables

### Các join quan trọng

| Join | Ý nghĩa |
|---|---|
| orders + customers | customer information |
| orders + payments | payment information |
| orders + reviews | review information |
| order_items + products | product information |

---

## 7.8 Create Master Dataset

### Mục tiêu

Tạo bảng trung tâm phục vụ:

- analytics
- machine learning
- dashboard

---

## 7.9 Save Silver Layer

Lưu cleaned data dạng Delta.

---

# 8. DAY 3 — FEATURE ENGINEERING

# Notebook: 03_feature_engineering

---

## 8.1 Mục tiêu

Biến dữ liệu business thành ML features.

---

# 8.2 Feature Engineering

## delivery_time

### Công thức

```python
actual_delivery - purchase_date
```

### Ý nghĩa

Thời gian giao hàng thực tế.

---

## delivery_delay

### Công thức

```python
actual_delivery - estimated_delivery
```

### Ý nghĩa

Số ngày giao trễ.

Đây là feature cực kỳ quan trọng.

---

## shipping_duration

### Công thức

```python
carrier_date - purchase_date
```

### Ý nghĩa

Tốc độ seller xử lý đơn hàng.

---

## order_total_value

### Công thức

```python
price + freight
```

### Ý nghĩa

Giá trị tổng đơn hàng.

---

## customer_total_orders

### Ý nghĩa

Mức độ loyal customer.

---

## customer_total_spent

### Ý nghĩa

Tổng số tiền khách đã chi tiêu.

---

## avg_review_score_customer

### Ý nghĩa

Hành vi đánh giá lịch sử của khách hàng.

Đây là feature mạnh nhất của model.

---

# 8.3 Label Definition

## Positive Review

```python
review_score >= 4
```

---

## Negative Review

```python
review_score < 4
```

---

# 8.4 Exploratory Data Analysis

## Phân tích chính

### Top Categories

Xác định ngành hàng phổ biến.

---

### Payment Methods

Phân tích phương thức thanh toán.

---

### Delivery Delay

Đánh giá hiệu suất vận chuyển.

---

### Review Distribution

Phân tích phân bố review.

---

# 8.5 Visualization

## Các biểu đồ

- histogram
- bar chart
- heatmap
- correlation matrix

---

# 9. DAY 4 — MACHINE LEARNING

# Notebook: 04_machine_learning

---

## 9.1 Mục tiêu

Train model dự đoán customer satisfaction.

---

# 9.2 Data Preparation

## StringIndexer

### Mục tiêu

Encode categorical feature.

Ví dụ:

```text
credit_card → 0
boleto → 1
```

---

## VectorAssembler

### Mục tiêu

Combine tất cả feature thành vector.

---

## Train/Test Split

### Mục tiêu

Tách dữ liệu:

- train set
- test set

---

# 9.3 Model Training

## Logistic Regression

### Vai trò

Baseline model.

---

## Random Forest

### Vai trò

Main model.

### Ưu điểm

- robust
- xử lý non-linear tốt
- interpretability tốt

---

## GBTClassifier

### Vai trò

Boosting model.

---

# 9.4 Model Evaluation

## Accuracy

Tỷ lệ dự đoán đúng.

---

## Precision

Prediction positive chính xác bao nhiêu.

---

## Recall

Bắt được bao nhiêu positive thật.

---

## F1-score

Cân bằng Precision và Recall.

---

## ROC-AUC

Khả năng phân biệt class.

---

# 9.5 Model Comparison

## Kết quả thực tế

Random Forest cho kết quả tốt nhất.

---

# 9.6 Feature Importance

## Feature mạnh nhất

| Feature | Ý nghĩa |
|---|---|
| avg_review_score_customer | historical behavior |
| delivery_delay | giao hàng trễ |
| delivery_time | tốc độ giao hàng |

---

## Nhận xét

Customer có lịch sử review tốt thường tiếp tục review tốt.

Delivery delay ảnh hưởng mạnh đến customer satisfaction.

---

# 9.7 Save Model

## Mục tiêu

Export model dùng cho API.

---

# 10. DAY 5 — API & MICROSERVICE

---

# 10.1 Mục tiêu

Deploy model thành realtime prediction service.

---

# 10.2 Cấu trúc API

```text
api/
│
├── app/
│   ├── main.py
│   ├── predictor.py
│   └── schema.py
│
├── models/
│
├── requirements.txt
│
└── Dockerfile
```

---

# 10.3 main.py

## Vai trò

FastAPI entry point.

---

## Endpoint

```text
POST /predict
```

---

# 10.4 schema.py

## Vai trò

Validate request input.

---

# 10.5 predictor.py

## Vai trò

- load Spark model
- preprocess input
- predict realtime

---

# 10.6 Dockerfile

## Vai trò

Containerize service.

---

# 10.7 Swagger UI

Sau khi chạy:

```bash
python -m uvicorn app.main:app --reload
```

Mở:

```text
http://127.0.0.1:8000/docs
```

---

# 11. DAY 6 — DASHBOARD & CLOUD

---

# 11.1 Dashboard

## Sales Dashboard

- total revenue
- top products
- top sellers

---

## Customer Dashboard

- review score
- delivery delay
- payment types

---

## ML Dashboard

- model accuracy
- prediction result
- feature importance

---

# 11.2 Cloud Deployment

## Platform

- Render
- Railway

---

# 12. DAY 7 — FINALIZATION

---

# 12.1 Documentation

Viết:

- project overview
- architecture
- ETL pipeline
- ML pipeline
- deployment

---

# 12.2 Presentation

## Nội dung slide

1. Business Problem
2. Dataset
3. Architecture
4. ETL Pipeline
5. Feature Engineering
6. Machine Learning
7. API
8. Dashboard
9. Demo
10. Conclusion

---

# 13. GIẢI THÍCH LUỒNG NOTEBOOK

---

# 01_data_understanding

Hiểu dữ liệu.

---

# 02_etl_pipeline

Xây dựng ETL và Data Warehouse.

---

# 03_feature_engineering

Tạo feature cho Machine Learning.

---

# 04_machine_learning

Train và evaluate model.

---

# 14. KỸ NĂNG THỂ HIỆN TRONG PROJECT

## Data Engineering

- Spark
- ETL
- Delta Lake

---

## Machine Learning

- Feature Engineering
- Classification
- Evaluation

---

## Backend Engineering

- FastAPI
- Docker

---

## Cloud

- Databricks
- Render
- Railway

---

## BI

- Power BI

---

# 15. KẾT LUẬN

Project đã xây dựng thành công một hệ thống Big Data E-commerce hoàn chỉnh theo hướng production-like.

Hệ thống có khả năng:

- xử lý dữ liệu lớn
- xây dựng ETL pipeline
- train ML model
- deploy realtime prediction API
- trực quan hóa dữ liệu

Đây là một project mang tính tổng hợp giữa:

- Data Engineering
- Machine Learning
- Backend Engineering
- Cloud Deployment
- Business Intelligence

Project phù hợp để:

- portfolio
- báo cáo môn học
- demo internship
- thực hành production workflow

