# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcode API Keys**: Khai báo thẳng `sk-...` trong mã nguồn.
2. **Stateful**: Lưu lịch sử chat, budget, hay rate limit vào biến lưu trữ tạm thời trên bộ nhớ RAM (`_rate_windows`, `_daily_cost` trong file `main.py`).
3. **Hardcode Port**: Không cấu hình linh hoạt biến môi trường `$PORT` mà fix cứng cổng `8000`.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config / Secrets | File `.env` lưu trên máy cá nhân | Environment Variables cài đặt trên nền tảng Cloud | Giúp mã nguồn an toàn khi đẩy lên Github, tránh lộ Key. |
| State Management | Lưu trong bộ nhớ RAM máy cá nhân | Lưu vào Database độc lập (Redis) | Giúp ứng dụng Scale nhiều bản sao (instances) vẫn chạy ổn định. |
| Networking | `localhost:8000` | Giao thức HTTPS, Load Balancer, Public Domain | Bảo mật đường truyền dữ liệu và định tuyến tới máy rảnh. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim`
2. Working directory: `/app`
3. Tại sao lại dùng multi-stage build? Để chỉ copy các thư viện đã được build xong từ `builder stage` sang `runtime stage`, bỏ lại toàn bộ các công cụ biên dịch nặng nề như gcc, giúp giảm triệt để dung lượng ảnh Docker (Image Size).

### Exercise 2.3: Image size comparison
- Develop (Dùng bản python:3.11 thường, single stage): ~1000 MB
- Production (Dùng bản slim kết hợp multi-stage build): ~160 MB
- Difference: Tiết kiệm được ~84% dung lượng

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: `https://[BẠN_ĐIỀN_LINK_RAILWAY_VÀO_ĐÂY]`
- Screenshot: Vui lòng xem ảnh trong thư mục `screenshots/`

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- Nếu gọi `/ask` không truyền Header `X-API-Key` -> Kết quả tự động chặn và trả về HTTP Status `401 Unauthorized`.
- Nếu truyền đủ Header -> Trả về JSON thành công kèm thời gian phản hồi.
- Nếu gửi quá nhiều (Rate Limit) -> Redis đếm số lượng token liên tục và kích hoạt lỗi `429 Too Many Requests`.

### Exercise 4.4: Cost guard implementation
Sử dụng thư viện `redis` kết hợp Redis Pipeline. Mỗi khi nhận request, quy đổi độ dài `question` và `answer` ra Token. Lấy số Token nhân với mức giá định sẵn để quy ra USD, sau đó cộng dồn `(incrbyfloat)` vào Redis key `daily_cost:YYYY-MM-DD`. 
Trước khi xử lý LLM, so sánh số tiền này với biến `DAILY_BUDGET_USD`, nếu vượt quá thì từ chối xử lý và chặn HTTP `503`.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Triển khai Stateless hoàn toàn thông qua cơ sở dữ liệu in-memory siêu tốc Redis, xoá bỏ biến Global Dictionary trên RAM.
- **Liveness Probe** (`/health`): Trả về HTTP 200 kèm uptime, request counts để báo hiệu cho Container Management Platform (như K8s, Railway) biết app vẫn còn sống, nếu sập sẽ tự restart.
- **Readiness Probe** (`/ready`): Gọi hàm `redis_client.ping()`, chỉ khi trả lời OK thì mới bắt đầu dẫn luồng kết nối (traffic routing) tới cho Agent, chống rớt gói tin lúc đang khởi động.
