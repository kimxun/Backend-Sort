# Backend-Sort

## 🛠 Cài Đặt

### 1. Cài dependencies

```bash
pip install -r requirements.txt 

backend/
├── app.py
├── algorithms/
│   ├── __init__.py
│   ├── interchange_sort.py
│   ├── selection_sort.py
│   └── quick_sort.py
├── requirements.txt
└── README.md

Chạy_sever: python app.py

Server chạy mặc định tại: http://localhost:5000

### 2. API Endpoints

Lấy_DS: GET /api/algorithms

Lấy_Detail: GET /api/algorithms/:id

Chạy_Sort: POST /api/sort