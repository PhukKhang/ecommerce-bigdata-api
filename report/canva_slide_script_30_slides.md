# Script tạo slide Canva - E-commerce Big Data API

Nguồn nội dung: `Báo cáo cuối kỳ Cloud - chỉnh lý theo project v2.docx`

Gợi ý dùng trên Canva:
- Chọn khổ `Presentation 16:9`.
- Phong cách: công nghệ, dữ liệu, điện toán đám mây; nền sáng, chữ đậm dễ đọc.
- Màu chủ đạo: xanh dương `#2563EB`, xanh lá `#16A34A`, xám đậm `#111827`, nền trắng/xám nhạt.
- Font gợi ý: Inter, Montserrat, Be Vietnam Pro hoặc Arial.
- Không đưa quá nhiều chữ lên slide. Phần `Nội dung trên slide` dùng để trình chiếu; phần `Lời thuyết trình` dùng để nói.
- Các hình cần chèn:
  - `report/figures/hinh_4_5_accuracy.png`
  - `report/figures/hinh_4_6_f1_score.png`
  - `report/figures/hinh_4_7_roc_auc.png`
  - Ảnh dashboard Power BI do nhóm chụp màn hình.
  - Ảnh Swagger UI hoặc Prediction UI do nhóm chụp màn hình.

## Prompt tổng để dán vào Canva Magic Design / Canva AI

Tạo bài thuyết trình khoảng 30 slide bằng tiếng Việt cho đề tài đồ án cuối kỳ: "Phân tích và Dự đoán Hành vi Người dùng E-commerce dựa trên bộ dữ liệu Olist". Bài trình bày thuộc môn Kiến trúc hướng dịch vụ và Điện toán đám mây. Nội dung cần thể hiện hệ thống phân tích dữ liệu lớn và dự đoán mức độ hài lòng khách hàng bằng PySpark, Databricks, Spark MLlib, FastAPI, Render và Power BI. Phong cách trình bày hiện đại, rõ ràng, phù hợp báo cáo kỹ thuật. Mỗi slide có tiêu đề ngắn, 3-5 ý chính, có chỗ đặt hình minh họa như kiến trúc hệ thống, pipeline ETL, biểu đồ so sánh model, ảnh dashboard, ảnh Swagger API và Prediction UI. Bài trình bày cần đi theo mạch: giới thiệu bài toán, ý nghĩa, dữ liệu Olist, yêu cầu hệ thống, kiến trúc SOA, ETL, feature engineering, xây dựng nhãn, huấn luyện model, đánh giá thực nghiệm, lựa chọn Random Forest, triển khai API lên Render, xây dựng dashboard Power BI, kết quả đạt được, hạn chế và hướng phát triển.

---

## Slide 1 - Trang bìa

**Nội dung trên slide**
- ĐỒ ÁN CUỐI KỲ
- Phân tích và Dự đoán Hành vi Người dùng E-commerce
- Dựa trên bộ dữ liệu Olist
- Môn học: Kiến trúc hướng dịch vụ và Điện toán đám mây
- Nhóm thực hiện: Nguyễn Tiến Dũng - 23650821; Nguyễn Trần Phúc Khang - 23660931
- Lớp: DHKHDL19A - Khóa 19

**Gợi ý thiết kế Canva**
- Dùng nền sáng hoặc nền gradient nhẹ xanh dương/xanh lá.
- Thêm icon cloud, database, shopping cart, chart.
- Có thể đặt một hình minh họa dashboard hoặc hệ thống dữ liệu ở nền mờ.

**Lời thuyết trình**
Kính chào thầy và các bạn. Nhóm em xin trình bày đồ án cuối kỳ với đề tài "Phân tích và Dự đoán Hành vi Người dùng E-commerce dựa trên bộ dữ liệu Olist". Đề tài tập trung xây dựng một hệ thống hoàn chỉnh từ xử lý dữ liệu lớn, huấn luyện mô hình học máy, triển khai API dự đoán trên cloud và trực quan hóa kết quả bằng Power BI.

---

## Slide 2 - Mục tiêu bài trình bày

**Nội dung trên slide**
- Trình bày bài toán phân tích dữ liệu thương mại điện tử.
- Giới thiệu bộ dữ liệu Olist và các bảng dữ liệu chính.
- Mô tả quy trình ETL, Feature Engineering và huấn luyện mô hình.
- Trình bày kết quả thực nghiệm và mô hình được lựa chọn.
- Demo hướng triển khai API dự đoán và dashboard Power BI.

**Gợi ý thiết kế Canva**
- Dùng layout timeline hoặc checklist 5 mục.
- Mỗi mục đi kèm icon: problem, data, pipeline, model, dashboard.

**Lời thuyết trình**
Nội dung trình bày gồm năm phần chính. Đầu tiên là giới thiệu bài toán và ý nghĩa thực tiễn. Tiếp theo là nguồn dữ liệu Olist và yêu cầu hệ thống. Sau đó nhóm trình bày kiến trúc, quy trình xử lý dữ liệu và xây dựng mô hình. Phần cuối tập trung vào kết quả thực nghiệm, triển khai cloud, dashboard và định hướng phát triển.

---

## Slide 3 - Bối cảnh thương mại điện tử

**Nội dung trên slide**
- E-commerce tạo ra lượng dữ liệu rất lớn từ đơn hàng, thanh toán, vận chuyển và đánh giá.
- Dữ liệu khách hàng phản ánh hành vi mua sắm và mức độ hài lòng.
- Doanh nghiệp cần công cụ phân tích để ra quyết định nhanh hơn.
- Dự đoán review giúp nhận diện sớm trải nghiệm tốt hoặc chưa tốt của khách hàng.

**Gợi ý thiết kế Canva**
- Minh họa luồng từ khách hàng -> đơn hàng -> thanh toán -> giao hàng -> đánh giá.
- Dùng icon người dùng, giỏ hàng, xe giao hàng, sao đánh giá.

**Lời thuyết trình**
Trong thương mại điện tử, mỗi giao dịch tạo ra nhiều loại dữ liệu khác nhau như thông tin khách hàng, sản phẩm, phương thức thanh toán, thời gian giao hàng và đánh giá sau mua. Nếu chỉ lưu trữ dữ liệu mà không phân tích, doanh nghiệp sẽ khó hiểu được nguyên nhân làm khách hàng hài lòng hoặc không hài lòng. Vì vậy, việc kết hợp phân tích dữ liệu và mô hình dự đoán giúp doanh nghiệp khai thác dữ liệu hiệu quả hơn.

---

## Slide 4 - Vấn đề cần giải quyết

**Nội dung trên slide**
- Dữ liệu nằm ở nhiều bảng khác nhau, cần được kết hợp và chuẩn hóa.
- Cần phân tích doanh thu, đơn hàng, phương thức thanh toán, đánh giá và giao hàng.
- Cần mô hình dự đoán review là Positive hoặc Negative.
- Cần triển khai kết quả thành API và dashboard dễ sử dụng.

**Gợi ý thiết kế Canva**
- Dùng sơ đồ "Problem -> Solution".
- Cột trái: dữ liệu phân tán, khó theo dõi, khó dự đoán.
- Cột phải: ETL, ML model, API, dashboard.

**Lời thuyết trình**
Bài toán không chỉ là huấn luyện một mô hình học máy đơn lẻ. Nhóm cần xây dựng toàn bộ quy trình từ dữ liệu thô đến sản phẩm có thể sử dụng. Dữ liệu ban đầu phân tán ở nhiều file CSV, cần được làm sạch và join lại. Sau đó nhóm xây dựng đặc trưng, huấn luyện mô hình dự đoán mức độ hài lòng và triển khai mô hình thành API để người dùng có thể nhập thông tin đơn hàng và nhận kết quả dự đoán.

---

## Slide 5 - Mục tiêu của đề tài

**Nội dung trên slide**
- Xây dựng pipeline xử lý dữ liệu Olist bằng PySpark trên Databricks.
- Tạo bộ dữ liệu tổng hợp phục vụ phân tích và Machine Learning.
- Huấn luyện và so sánh Logistic Regression, Random Forest, GBTClassifier.
- Triển khai mô hình Random Forest qua FastAPI trên Render.
- Xây dựng dashboard Power BI để trực quan hóa dữ liệu kinh doanh.

**Gợi ý thiết kế Canva**
- Dùng 5 khối mục tiêu nối với nhau theo chiều ngang.
- Nhấn mạnh output cuối: API dự đoán + dashboard.

**Lời thuyết trình**
Mục tiêu chính của đề tài là xây dựng một hệ thống phân tích và dự đoán hoàn chỉnh. Về dữ liệu, nhóm xử lý bộ dữ liệu Olist bằng PySpark trên Databricks. Về mô hình, nhóm thử nghiệm ba thuật toán phổ biến và chọn mô hình phù hợp nhất để triển khai. Về ứng dụng, nhóm xây dựng API dự đoán bằng FastAPI, deploy trên Render và tạo dashboard Power BI để hỗ trợ theo dõi các chỉ số kinh doanh.

---

## Slide 6 - Bộ dữ liệu Olist

**Nội dung trên slide**
- Nguồn dữ liệu: Olist Brazilian E-commerce Dataset.
- Thời gian ghi nhận giao dịch: 2016 - 2018.
- Quy mô khoảng:
  - 100.000+ đơn hàng.
  - 99.000+ khách hàng.
  - 32.000+ sản phẩm.
  - 3.000+ người bán.
- Dữ liệu phù hợp cho phân tích E-commerce và dự đoán review.

**Gợi ý thiết kế Canva**
- Dùng infographic 4 số lớn.
- Có thể dùng bản đồ Brazil hoặc icon marketplace.

**Lời thuyết trình**
Bộ dữ liệu nhóm sử dụng là Olist Brazilian E-commerce Dataset, một bộ dữ liệu công khai rất phổ biến trong các bài toán phân tích thương mại điện tử. Dữ liệu ghi nhận các giao dịch từ năm 2016 đến 2018, bao gồm hơn 100 nghìn đơn hàng, gần 100 nghìn khách hàng, hơn 32 nghìn sản phẩm và hơn 3 nghìn người bán. Quy mô và cấu trúc nhiều bảng của bộ dữ liệu này phù hợp để áp dụng Big Data, ETL và Machine Learning.

---

## Slide 7 - Các bảng dữ liệu chính

**Nội dung trên slide**
- `customers`: thông tin khách hàng.
- `orders`: thông tin đơn hàng.
- `order_items`: chi tiết sản phẩm trong đơn hàng.
- `products`: thông tin sản phẩm.
- `sellers`: thông tin người bán.
- `payments`: thông tin thanh toán.
- `reviews`: đánh giá của khách hàng.
- `geolocation`: thông tin vị trí địa lý.

**Gợi ý thiết kế Canva**
- Dùng sơ đồ database với 8 bảng.
- Đặt các khóa liên kết: `order_id`, `customer_id`, `product_id`, `seller_id`.

**Lời thuyết trình**
Dữ liệu Olist không nằm trong một bảng duy nhất mà được chia thành nhiều bảng theo đúng nghiệp vụ thương mại điện tử. Ví dụ bảng khách hàng chứa thông tin người mua, bảng đơn hàng chứa trạng thái và thời gian đơn, bảng thanh toán chứa phương thức và giá trị thanh toán, bảng reviews chứa điểm đánh giá. Các bảng được liên kết bằng những khóa như order_id, customer_id, product_id và seller_id.

---

## Slide 8 - Câu hỏi phân tích chính

**Nội dung trên slide**
- Tổng doanh thu và số lượng đơn hàng thay đổi như thế nào theo thời gian?
- Phương thức thanh toán nào được sử dụng nhiều nhất?
- Danh mục sản phẩm nào tạo doanh thu cao?
- Khu vực/bang nào có doanh thu lớn?
- Tỷ lệ giao hàng đúng hạn và trễ ra sao?
- Điểm đánh giá khách hàng phân bố như thế nào?

**Gợi ý thiết kế Canva**
- Dùng layout dạng 6 câu hỏi trong các ô nhỏ.
- Thêm icon chart, payment, category, map, delivery, star.

**Lời thuyết trình**
Bên cạnh bài toán dự đoán, nhóm cũng đặt ra các câu hỏi phân tích phục vụ dashboard. Các câu hỏi này giúp hiểu rõ tình hình kinh doanh như doanh thu theo thời gian, top danh mục, top seller, phân bố thanh toán, tình trạng giao hàng và phân bố điểm đánh giá. Đây là các thông tin quan trọng để người quản lý có thể theo dõi hoạt động thương mại điện tử một cách trực quan.

---

## Slide 9 - Yêu cầu hệ thống

**Nội dung trên slide**
- Thu thập và lưu trữ dữ liệu từ nhiều bảng CSV.
- Xử lý dữ liệu lớn bằng PySpark/Databricks.
- Làm sạch, chuẩn hóa và kết hợp dữ liệu.
- Huấn luyện mô hình dự đoán review.
- Cung cấp API dự đoán thời gian thực.
- Xây dựng dashboard Power BI.

**Gợi ý thiết kế Canva**
- Dùng checklist chia 2 nhóm: Data/ML và Cloud/Dashboard.

**Lời thuyết trình**
Hệ thống cần đáp ứng cả yêu cầu chức năng và phi chức năng. Về chức năng, hệ thống phải xử lý được dữ liệu, tạo báo cáo phân tích và dự đoán review. Về kỹ thuật, hệ thống cần tận dụng xử lý phân tán bằng Spark, triển khai được trên môi trường cloud và có khả năng mở rộng khi dữ liệu tăng lên. Đây là lý do nhóm chọn Databricks, PySpark, FastAPI, Render và Power BI.

---

## Slide 10 - Kiến trúc tổng quan hệ thống

**Nội dung trên slide**
- Data Source: bộ dữ liệu Olist.
- Data Processing: PySpark trên Databricks.
- Feature Engineering: tạo đặc trưng hành vi mua hàng.
- Model Training: Spark MLlib.
- Prediction API: FastAPI deploy trên Render.
- Visualization: Power BI Dashboard.

**Gợi ý thiết kế Canva**
- Vẽ sơ đồ pipeline từ trái sang phải:
  `Olist CSV -> Databricks/PySpark -> Feature Store/Dataset -> ML Model -> FastAPI -> Prediction UI`
  và nhánh `Processed Data -> Power BI`.

**Lời thuyết trình**
Kiến trúc tổng quan của hệ thống đi theo luồng dữ liệu từ nguồn đến ứng dụng. Dữ liệu Olist được đưa vào Databricks để xử lý bằng PySpark. Sau khi làm sạch và kết hợp, hệ thống xây dựng các đặc trưng phục vụ phân tích và huấn luyện mô hình. Mô hình tốt nhất được đóng gói và triển khai thông qua FastAPI trên Render. Song song đó, dữ liệu tổng hợp được đưa vào Power BI để xây dựng dashboard.

---

## Slide 11 - Kiến trúc hướng dịch vụ SOA

**Nội dung trên slide**
- Data Ingestion Service: tiếp nhận dữ liệu.
- ETL/Data Processing Service: làm sạch và kết hợp dữ liệu.
- Feature Engineering Service: tạo đặc trưng.
- Model Training Service: huấn luyện và đánh giá model.
- Prediction Service: cung cấp API dự đoán.
- Visualization Service: trực quan hóa bằng Power BI.

**Gợi ý thiết kế Canva**
- Dùng sơ đồ 6 service độc lập.
- Mỗi service là một block, kết nối bằng mũi tên/API.

**Lời thuyết trình**
Đề tài áp dụng tư duy kiến trúc hướng dịch vụ. Thay vì gom toàn bộ chức năng vào một khối, hệ thống được chia thành các dịch vụ độc lập theo nhiệm vụ. Cách tổ chức này giúp hệ thống dễ mở rộng, dễ bảo trì và phù hợp với điện toán đám mây. Ví dụ Prediction Service có thể triển khai riêng để phục vụ dự đoán, trong khi Visualization Service tập trung vào dashboard và báo cáo.

---

## Slide 12 - Quy trình ETL

**Nội dung trên slide**
- Extract: đọc các file CSV vào Spark DataFrame.
- Transform:
  - Xử lý NULL.
  - Loại bỏ trùng lặp.
  - Chuẩn hóa kiểu dữ liệu.
  - Chuyển đổi ngày tháng.
  - Join nhiều bảng dữ liệu.
- Load: lưu dữ liệu xử lý ở dạng Parquet/Delta Table hoặc CSV dashboard.

**Gợi ý thiết kế Canva**
- Sơ đồ 3 bước Extract - Transform - Load.
- Chèn icon CSV, Spark, Delta/Parquet, Power BI.

**Lời thuyết trình**
ETL là bước nền tảng của hệ thống. Ở bước Extract, dữ liệu từ các file CSV được đọc vào Spark DataFrame. Ở bước Transform, nhóm xử lý dữ liệu thiếu, loại bỏ trùng lặp, chuẩn hóa kiểu dữ liệu và kết hợp các bảng như orders, customers, payments, reviews, order_items và products. Sau khi xử lý, dữ liệu được lưu lại để phục vụ phân tích, dashboard và huấn luyện mô hình.

---

## Slide 13 - Xử lý dữ liệu bằng PySpark trên Databricks

**Nội dung trên slide**
- PySpark hỗ trợ xử lý dữ liệu phân tán.
- Databricks cung cấp môi trường notebook và Spark cluster.
- Phù hợp với dữ liệu nhiều bảng, nhiều bản ghi.
- Giảm tải so với xử lý thủ công bằng Excel hoặc Pandas thuần.
- Dễ tích hợp với Spark MLlib để huấn luyện model.

**Gợi ý thiết kế Canva**
- Dùng hình minh họa cluster: nhiều node xử lý dữ liệu.
- Thêm logo/nhãn PySpark, Databricks, MLlib.

**Lời thuyết trình**
Do bộ dữ liệu có quy mô lớn và gồm nhiều bảng liên kết, nhóm sử dụng PySpark trên Databricks để xử lý. Spark cho phép xử lý dữ liệu theo mô hình phân tán, phù hợp hơn so với cách xử lý thủ công. Databricks hỗ trợ môi trường notebook, giúp nhóm dễ triển khai các bước đọc dữ liệu, làm sạch, join bảng, xây dựng đặc trưng và huấn luyện mô hình bằng Spark MLlib.

---

## Slide 14 - Feature Engineering

**Nội dung trên slide**
- Delivery Time: thời gian giao hàng thực tế.
- Delivery Delay: độ trễ so với ngày dự kiến.
- Shipping Duration: thời gian vận chuyển.
- Total Order Value: giá trị đơn hàng.
- Payment Information: loại thanh toán, số kỳ trả góp, giá trị thanh toán.
- Seller Performance: số đơn, đánh giá trung bình, tỷ lệ giao đúng hạn.
- Customer Statistics: tổng số đơn, tổng chi tiêu, điểm review trung bình.

**Gợi ý thiết kế Canva**
- Dùng sơ đồ từ dữ liệu thô -> đặc trưng đầu vào.
- Mỗi nhóm đặc trưng dùng icon riêng.

**Lời thuyết trình**
Feature Engineering là bước rất quan trọng vì chất lượng đặc trưng ảnh hưởng trực tiếp đến chất lượng dự đoán. Nhóm không chỉ dùng dữ liệu gốc mà còn tạo thêm các đặc trưng mới phản ánh trải nghiệm khách hàng. Ví dụ delivery delay cho biết đơn hàng có bị trễ không, total order value phản ánh giá trị đơn, payment information cho biết hành vi thanh toán, còn seller performance thể hiện chất lượng hoạt động của người bán.

---

## Slide 15 - Xây dựng nhãn dự đoán

**Nội dung trên slide**
- Trường gốc: `review_score`.
- Quy tắc tạo nhãn:
  - `review_score >= 4` -> Positive Review `(1)`.
  - `review_score < 4` -> Negative Review `(0)`.
- Bài toán được chuyển thành Binary Classification.
- Output model: Positive hoặc Negative, kèm xác suất và confidence.

**Gợi ý thiết kế Canva**
- Dùng hình thang phân loại:
  `1-3 sao -> Negative`, `4-5 sao -> Positive`.
- Thêm icon sao đánh giá.

**Lời thuyết trình**
Mục tiêu của mô hình là dự đoán mức độ hài lòng của khách hàng. Vì dữ liệu có trường review_score từ 1 đến 5, nhóm chuyển bài toán thành phân loại nhị phân. Nếu review_score lớn hơn hoặc bằng 4 thì được gán nhãn Positive, thể hiện khách hàng hài lòng. Nếu nhỏ hơn 4 thì gán nhãn Negative. Cách xây dựng nhãn này giúp mô hình tập trung vào việc nhận diện review tốt hoặc không tốt.

---

## Slide 16 - Pipeline Machine Learning

**Nội dung trên slide**
- Input: dữ liệu đã ETL và feature engineering.
- Tiền xử lý:
  - StringIndexer.
  - One-Hot Encoding.
  - VectorAssembler.
- Chia dữ liệu:
  - 80% training.
  - 20% testing.
- Huấn luyện 3 mô hình.
- Đánh giá và chọn mô hình triển khai.

**Gợi ý thiết kế Canva**
- Vẽ pipeline ML:
  `Processed Dataset -> Encoding -> VectorAssembler -> Train/Test Split -> Model Training -> Evaluation -> Best Model`.

**Lời thuyết trình**
Sau khi có tập dữ liệu tổng hợp, nhóm xây dựng pipeline học máy. Các thuộc tính dạng chuỗi như payment_type hoặc product_category cần được mã hóa bằng StringIndexer và One-Hot Encoding. Sau đó các đặc trưng được gom lại bằng VectorAssembler để đưa vào mô hình Spark MLlib. Dữ liệu được chia theo tỷ lệ 80/20, trong đó 80% dùng để huấn luyện và 20% dùng để kiểm thử.

---

## Slide 17 - Các mô hình được thử nghiệm

**Nội dung trên slide**
- Logistic Regression:
  - Baseline tuyến tính.
  - Nhanh, dễ giải thích.
- Random Forest:
  - Ensemble nhiều cây quyết định.
  - Ổn định, giảm overfitting.
  - Có Feature Importance.
- GBTClassifier:
  - Boosting nhiều cây quyết định.
  - Học tốt quan hệ phức tạp.
  - Huấn luyện tốn tài nguyên hơn.

**Gợi ý thiết kế Canva**
- Dùng bảng so sánh 3 cột.
- Mỗi mô hình có icon riêng: line, forest/tree, boosted trees.

**Lời thuyết trình**
Nhóm lựa chọn ba thuật toán để so sánh. Logistic Regression được dùng như một mô hình baseline vì đơn giản và dễ giải thích. Random Forest là mô hình ensemble dựa trên nhiều cây quyết định, có khả năng chống overfitting và hoạt động ổn định. GBTClassifier cũng dựa trên cây quyết định nhưng huấn luyện theo cơ chế boosting, thường có khả năng học các quan hệ phi tuyến tốt hơn nhưng tốn tài nguyên hơn.

---

## Slide 18 - Các chỉ số đánh giá

**Nội dung trên slide**
- Accuracy: tỷ lệ dự đoán đúng trên toàn bộ tập kiểm thử.
- Precision: mức độ chính xác của các dự đoán Positive.
- Recall: khả năng phát hiện đầy đủ lớp Positive.
- F1-Score: cân bằng giữa Precision và Recall.
- ROC-AUC: khả năng phân biệt giữa hai lớp.
- Balanced Accuracy: cân bằng hiệu quả giữa Positive và Negative.

**Gợi ý thiết kế Canva**
- Dùng card nhỏ cho từng metric.
- Metric quan trọng nên tô màu: F1, ROC-AUC, Balanced Accuracy.

**Lời thuyết trình**
Để đánh giá mô hình, nhóm không chỉ nhìn vào Accuracy mà còn xem nhiều chỉ số khác. Accuracy cho biết tỷ lệ dự đoán đúng tổng thể, nhưng nếu dữ liệu lệch lớp thì Accuracy có thể chưa phản ánh đầy đủ. Vì vậy nhóm dùng thêm F1-Score, ROC-AUC và Balanced Accuracy. Trong project này, Random Forest được chọn chủ yếu nhờ Balanced Accuracy cao nhất và độ ổn định khi triển khai.

---

## Slide 19 - Cấu hình thực nghiệm

**Nội dung trên slide**
- Ngôn ngữ: Python 3.12.
- Nền tảng xử lý: Apache Spark / PySpark.
- Môi trường: Databricks.
- Thư viện ML: Spark MLlib.
- Dữ liệu sau xử lý:
  - 99.441 dòng ML.
  - 79.465 dòng train.
  - 19.976 dòng test.
- Tỷ lệ train/test: khoảng 80/20.

**Gợi ý thiết kế Canva**
- Dùng layout "Experiment Setup".
- Có 2 khối: Environment và Dataset Split.

**Lời thuyết trình**
Quá trình thực nghiệm được thực hiện bằng Python 3.12, PySpark và Spark MLlib trên Databricks. Sau khi xử lý và tạo đặc trưng, tập dữ liệu dùng cho Machine Learning có 99.441 dòng. Trong đó 79.465 dòng dùng để huấn luyện và 19.976 dòng dùng để kiểm thử. Cách chia này giúp đánh giá mô hình trên dữ liệu chưa từng được mô hình nhìn thấy trong quá trình học.

---

## Slide 20 - Kết quả Accuracy

**Nội dung trên slide**
- Logistic Regression: 82.51%.
- Random Forest: 84.20%.
- GBTClassifier: 84.23%.
- GBTClassifier nhỉnh hơn nhẹ về Accuracy.
- Random Forest vẫn rất sát GBT và ổn định khi triển khai.

**Gợi ý thiết kế Canva**
- Chèn hình: `report/figures/hinh_4_5_accuracy.png`.
- Caption: "Hình 4.5. Biểu đồ so sánh Accuracy giữa các mô hình."

**Lời thuyết trình**
Về Accuracy, cả ba mô hình đều đạt kết quả khá tốt. Logistic Regression đạt 82.51%, trong khi Random Forest và GBTClassifier đạt khoảng 84.2%. GBTClassifier cao nhất về Accuracy nhưng mức chênh lệch so với Random Forest rất nhỏ, chỉ khoảng 0.03 điểm phần trăm. Vì vậy nhóm không chỉ dựa vào Accuracy để lựa chọn mô hình cuối cùng.

---

## Slide 21 - Kết quả F1-Score

**Nội dung trên slide**
- Logistic Regression: 90.26%.
- Random Forest: 91.08%.
- GBTClassifier: 91.11%.
- Cả ba mô hình có F1-Score cao.
- Random Forest và GBTClassifier gần như tương đương.

**Gợi ý thiết kế Canva**
- Chèn hình: `report/figures/hinh_4_6_f1_score.png`.
- Caption: "Hình 4.6. Biểu đồ so sánh F1-Score giữa các mô hình."

**Lời thuyết trình**
F1-Score thể hiện sự cân bằng giữa Precision và Recall. Kết quả cho thấy cả ba mô hình đều có F1-Score cao, đặc biệt Random Forest và GBTClassifier đều trên 91%. Điều này cho thấy các đặc trưng được xây dựng có khả năng phản ánh tốt hành vi và trải nghiệm của khách hàng. Tuy nhiên, F1-Score vẫn cần được xem cùng các metric khác để tránh đánh giá lệch khi dữ liệu mất cân bằng.

---

## Slide 22 - Kết quả ROC-AUC

**Nội dung trên slide**
- Logistic Regression: 60.63%.
- Random Forest: 67.02%.
- GBTClassifier: 67.47%.
- GBTClassifier cao nhất về ROC-AUC.
- ROC-AUC ở mức trung bình khá, cho thấy bài toán vẫn còn khó.

**Gợi ý thiết kế Canva**
- Chèn hình: `report/figures/hinh_4_7_roc_auc.png`.
- Caption: "Hình 4.7. Biểu đồ so sánh ROC-AUC giữa các mô hình."

**Lời thuyết trình**
ROC-AUC đánh giá khả năng phân biệt giữa hai lớp Positive và Negative. Ở chỉ số này, GBTClassifier đạt 67.47%, Random Forest đạt 67.02% và Logistic Regression đạt 60.63%. Kết quả cho thấy các mô hình cây tốt hơn mô hình tuyến tính. Tuy nhiên ROC-AUC chưa quá cao, nghĩa là bài toán vẫn còn thách thức, đặc biệt trong việc nhận diện lớp Negative Review.

---

## Slide 23 - Bảng tổng hợp kết quả

**Nội dung trên slide**
| Model | Accuracy | F1-Score | ROC-AUC |
|---|---:|---:|---:|
| Logistic Regression | 82.51% | 90.26% | 60.63% |
| Random Forest | 84.20% | 91.08% | 67.02% |
| GBTClassifier | 84.23% | 91.11% | 67.47% |

**Gợi ý thiết kế Canva**
- Dùng bảng sạch, không quá nhiều viền.
- Tô nền hàng Random Forest để nhấn mạnh mô hình triển khai.

**Lời thuyết trình**
Bảng tổng hợp cho thấy GBTClassifier nhỉnh hơn nhẹ ở Accuracy, F1-Score và ROC-AUC. Tuy nhiên, khi xét thêm Balanced Accuracy và yêu cầu triển khai thực tế, Random Forest được lựa chọn vì đạt Balanced Accuracy cao nhất, kết quả ổn định và dễ triển khai hơn. Đây là điểm quan trọng: mô hình tốt nhất để triển khai không nhất thiết chỉ là mô hình có Accuracy cao nhất.

---

## Slide 24 - Lựa chọn mô hình Random Forest

**Nội dung trên slide**
- Random Forest được chọn làm mô hình triển khai chính thức.
- Lý do:
  - Balanced Accuracy cao nhất: 58.96%.
  - F1-Score cao và ổn định: 91.08%.
  - Giảm overfitting tốt hơn mô hình đơn lẻ.
  - Có thể giải thích bằng Feature Importance.
  - Phù hợp với môi trường triển khai API.

**Gợi ý thiết kế Canva**
- Dùng layout "Why Random Forest?"
- Có biểu tượng check cho từng lý do.

**Lời thuyết trình**
Mặc dù GBTClassifier cao hơn một chút ở vài metric tổng quát, nhóm chọn Random Forest làm mô hình triển khai chính thức. Lý do là Random Forest có Balanced Accuracy cao nhất, nghĩa là mô hình cân bằng hơn giữa hai lớp. Ngoài ra, mô hình này ổn định, ít overfitting hơn, có thể giải thích bằng Feature Importance và phù hợp hơn với điều kiện triển khai demo trên Render.

---

## Slide 25 - Triển khai Prediction API

**Nội dung trên slide**
- Framework: FastAPI.
- Model: Random Forest PipelineModel.
- Deploy cloud: Render.
- Endpoint chính:
  - `GET /health`: kiểm tra trạng thái API.
  - `GET /docs`: Swagger UI.
  - `POST /predict`: dự đoán review.
- API URL: `https://ecommerce-review-prediction-api.onrender.com`

**Gợi ý thiết kế Canva**
- Chèn screenshot Swagger UI hoặc trang `/health`.
- Dùng sơ đồ client -> FastAPI -> model -> response JSON.

**Lời thuyết trình**
Sau khi chọn mô hình Random Forest, nhóm đóng gói mô hình và triển khai bằng FastAPI. API được deploy trên Render để có thể truy cập qua internet. Hệ thống cung cấp ba endpoint chính: `/health` để kiểm tra trạng thái, `/docs` để xem Swagger UI và `/predict` để gửi dữ liệu đầu vào và nhận kết quả dự đoán. Đây là phần thể hiện khả năng đưa mô hình Machine Learning thành một dịch vụ cloud thực tế.

---

## Slide 26 - Dữ liệu đầu vào và đầu ra API

**Nội dung trên slide**
- Input mẫu:
  - `payment_type`
  - `payment_installments`
  - `number_of_items`
  - `avg_item_price`
  - `delivery_time`
  - `delivery_delay`
  - `shipping_duration`
  - `order_total_value`
  - `customer_total_orders`
  - `customer_total_spent`
  - `avg_review_score_customer`
- Output:
  - `prediction`
  - `probabilities`
  - `confidence`
  - `model`

**Gợi ý thiết kế Canva**
- Dùng 2 khối JSON: Request và Response.
- Highlight kết quả `positive_review` và confidence.

**Lời thuyết trình**
API nhận vào các thông tin liên quan đến đơn hàng, thanh toán, giao hàng và lịch sử khách hàng. Sau khi xử lý đầu vào, mô hình trả về nhãn dự đoán là positive_review hoặc negative_review, xác suất cho từng lớp và mức độ confidence. Ví dụ trong quá trình kiểm thử, API trả về positive_review với xác suất khoảng 82.76% và confidence ở mức high.

---

## Slide 27 - Prediction UI

**Nội dung trên slide**
- Giao diện nhập thông tin đơn hàng.
- Người dùng nhập endpoint API Render.
- Nhấn `Predict Review` để gửi request.
- Hiển thị:
  - Kết quả Positive/Negative.
  - Confidence.
  - Xác suất từng lớp.
  - JSON response.
- Hỗ trợ demo trực quan hơn Swagger.

**Gợi ý thiết kế Canva**
- Chèn screenshot Prediction UI mà nhóm đã chạy thành công.
- Nếu có chỗ, đặt ảnh kết quả positive review high confidence.

**Lời thuyết trình**
Ngoài Swagger UI, nhóm xây dựng thêm giao diện Prediction UI để việc demo trực quan hơn. Người dùng có thể nhập thông tin đơn hàng, chọn phương thức thanh toán và gửi request đến API. Kết quả trả về được hiển thị dưới dạng dễ đọc gồm nhãn dự đoán, mức confidence, thanh xác suất Positive/Negative và JSON chi tiết. Điều này giúp người xem hiểu rõ cách model hoạt động trong ứng dụng thực tế.

---

## Slide 28 - Power BI Dashboard

**Nội dung trên slide**
- Dashboard phân tích dữ liệu kinh doanh từ Olist.
- Các chỉ số chính:
  - Tổng doanh thu.
  - Tổng đơn hàng.
  - Doanh thu theo tháng.
  - Doanh thu theo phương thức thanh toán.
  - Tình trạng giao hàng.
  - Top seller/top category.
  - Phân bố điểm đánh giá.
- File: `report/Ecommerce_BigData_Dashboard.pbix`

**Gợi ý thiết kế Canva**
- Chèn screenshot dashboard Power BI.
- Dùng caption: "Dashboard phân tích dữ liệu E-commerce".

**Lời thuyết trình**
Phần dashboard được xây dựng bằng Power BI nhằm trực quan hóa các kết quả phân tích. Dashboard cho phép theo dõi tổng doanh thu, số đơn hàng, doanh thu theo thời gian, phân bố phương thức thanh toán, tình trạng giao hàng, top danh mục, top seller và phân bố review score. Đây là thành phần hỗ trợ người dùng khai thác dữ liệu và đưa ra quyết định nhanh hơn.

---

## Slide 29 - Lợi ích của hệ thống

**Nội dung trên slide**
- Kết hợp BI và Machine Learning trong cùng một project.
- Xử lý dữ liệu lớn bằng PySpark/Databricks.
- Dự đoán mức độ hài lòng khách hàng qua API cloud.
- Dashboard giúp quan sát dữ liệu nhanh và trực quan.
- Kiến trúc SOA giúp hệ thống dễ mở rộng, bảo trì và tích hợp.

**Gợi ý thiết kế Canva**
- Dùng 5 benefit cards.
- Icon: analytics, spark, AI, dashboard, cloud.

**Lời thuyết trình**
Điểm mạnh của hệ thống là không dừng lại ở phân tích dữ liệu hoặc mô hình học máy riêng lẻ, mà kết hợp cả hai thành một hệ thống hoàn chỉnh. Dashboard giúp theo dõi dữ liệu quá khứ và hiện tại, còn API dự đoán giúp khai thác model cho các tình huống mới. Việc xây dựng theo hướng dịch vụ và triển khai trên cloud giúp hệ thống có khả năng mở rộng và phù hợp với bối cảnh ứng dụng thực tế.

---

## Slide 30 - Kết luận và hướng phát triển

**Nội dung trên slide**
- Kết quả đạt được:
  - Hoàn thành ETL dữ liệu Olist.
  - Xây dựng đặc trưng và nhãn dự đoán.
  - Huấn luyện 3 mô hình ML.
  - Chọn Random Forest để triển khai.
  - Deploy FastAPI trên Render.
  - Xây dựng dashboard Power BI.
- Hướng phát triển:
  - Mở rộng dữ liệu từ nhiều nền tảng.
  - Thử nghiệm Deep Learning.
  - Dự đoán giao hàng trễ, CLV, repeat purchase.
  - Streaming với Kafka/Spark Structured Streaming.
  - Triển khai Microservices với Docker/Kubernetes.

**Gợi ý thiết kế Canva**
- Dùng slide tổng kết 2 cột: "Đã hoàn thành" và "Phát triển tiếp".
- Kết thúc bằng dòng: "Thank you - Q&A".

**Lời thuyết trình**
Tổng kết lại, nhóm đã hoàn thành một quy trình tương đối đầy đủ từ thu thập dữ liệu, xử lý bằng PySpark, xây dựng đặc trưng, huấn luyện mô hình, triển khai API dự đoán và xây dựng dashboard Power BI. Mô hình Random Forest được chọn để triển khai do có kết quả ổn định và phù hợp với yêu cầu demo. Trong tương lai, hệ thống có thể mở rộng dữ liệu, thử nghiệm thêm mô hình học sâu, xây dựng bài toán dự đoán nâng cao và triển khai theo kiến trúc microservices để tăng khả năng mở rộng. Nhóm em xin kết thúc phần trình bày và sẵn sàng nhận câu hỏi từ thầy và các bạn.

---

# Gợi ý phân bổ thời gian báo cáo

- Slide 1-2: 1 phút.
- Slide 3-5: 2 phút.
- Slide 6-9: 3 phút.
- Slide 10-16: 5 phút.
- Slide 17-24: 5 phút.
- Slide 25-28: 4 phút.
- Slide 29-30: 2 phút.

Tổng thời lượng phù hợp: khoảng 18-22 phút nếu trình bày đầy đủ; có thể rút xuống 12-15 phút bằng cách nói ngắn phần Slide 11-18.

# Thứ tự demo đề xuất khi báo cáo

1. Mở dashboard Power BI trước để cho thấy kết quả BI.
2. Mở API `/health` để chứng minh service đang chạy.
3. Mở `/docs` để giới thiệu Swagger UI.
4. Mở Prediction UI và chạy một mẫu dự đoán.
5. Quay lại slide kết luận để tổng hợp giá trị hệ thống.

# Câu hỏi có thể bị hỏi và gợi ý trả lời

**1. Vì sao chọn Random Forest trong khi GBTClassifier có Accuracy cao hơn?**

Random Forest được chọn vì Balanced Accuracy cao nhất, kết quả ổn định và dễ triển khai hơn trong môi trường demo API. GBTClassifier nhỉnh hơn nhẹ ở Accuracy, F1 và ROC-AUC, nhưng chênh lệch nhỏ, trong khi Random Forest cân bằng hơn giữa hai lớp.

**2. Vì sao ROC-AUC chưa cao như Accuracy/F1?**

Dữ liệu có xu hướng lệch về Positive Review nên Accuracy và F1 có thể cao, nhưng việc phân biệt chính xác giữa Positive và Negative vẫn khó hơn. ROC-AUC phản ánh khả năng tách hai lớp nên kết quả ở mức trung bình khá.

**3. API chạy chậm ở lần đầu có phải lỗi không?**

Không hẳn. Khi deploy trên Render gói miễn phí, service có thể bị sleep sau một thời gian không dùng. Lần gọi đầu cần khởi động container và Spark session nên lâu hơn. Các lần sau thường nhanh hơn nếu service còn đang hoạt động.

**4. Dashboard dùng để làm gì nếu đã có model dự đoán?**

Dashboard dùng để phân tích dữ liệu tổng quan và theo dõi chỉ số kinh doanh, còn model dùng để dự đoán cho trường hợp mới. Hai phần bổ trợ cho nhau: BI giúp hiểu dữ liệu, ML giúp dự đoán.

**5. Hệ thống có thể áp dụng thực tế chưa?**

Hiện tại hệ thống ở mức demo/prototype. Để dùng thực tế cần bổ sung dữ liệu mới liên tục, giám sát model, tối ưu hạ tầng cloud, bảo mật API và kiểm thử trên môi trường production.

