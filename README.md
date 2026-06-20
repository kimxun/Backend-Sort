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
B1: Chuyển file env.example thành .env hoặc tạo file .env mới
B2: Thêm các giá trị mà tui đã gửi trong group vào
B3: Mở xampp bật apache với mysql rồi tạo database trùng tên với tên trong env
B4: Import file sql vào là xong

Các bước muốn tối ưu tốc độ xử lý api
B1: Tải docker về window rồi restart máy
B2: Cài xong docker sẽ hiện 1 powershell kêu là chỉ cần nhấn bất kỳ nút nào thì hãy nhấn đại phím đi nó sẽ tự động cài wsl(Windows Subsystem for Linux) lun ròi sau đó restart máy
B3: Vào backend cài "docker run -d -p 6379:6379 redis"
B4: Cài lại file requirement.txt

//**Lưu ý: phải có docker và wsl thì mới xài redis cache được thư viện thì đã thêm vô file requirement rồi nên chỉ cần chạy lại file đó thôi
