# Dashboard

Dashboard web tĩnh đọc dữ liệu tổng hợp từ `data/dashboard_data.json`.

## Mở Dashboard

Từ thư mục project:

```powershell
python -m http.server 5500 --directory dashboards
```

Mở [http://127.0.0.1:5500](http://127.0.0.1:5500).

## Cập Nhật Dữ Liệu

```powershell
python ecomerce/build_dashboard_data.py `
  --dataset-dir C:\temp\olist\files `
  --metrics ecomerce-api\models\best_model_metrics.json `
  --output-dir dashboards
```

Các file trong `powerbi/` là bảng tổng hợp có thể import trực tiếp vào Power BI.
