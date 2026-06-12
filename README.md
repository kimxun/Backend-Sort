Cài đặt Python dependencies

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
python -m pip install -r requirements.txt

Các bước kết nối csdl
B1: Chuyển file env.example thành .env
B2: Thêm các giá trị vào rồi lưu