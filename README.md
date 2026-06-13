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
python -m pip install -rr equirements.txt

Các bước kết nối csdl
B1: Chuyển file env.example thành .env hoặc tạo file .env mới
B2: Thêm các giá trị mà tui đã gửi trong group vào
B3: Mở xampp bật apache với mysql rồi tạo database trùng tên với tên trong env
B4: Import file sql vào là xong
