# Deployment Information

## Public URL
`https://agent-production-0f55.up.railway.app`

*(Lưu ý: Copy đường dẫn Domain mà Railway cấp cho bạn sau khi Deploy thành công và dán đè lên đoạn văn bản trên)*

## Platform
Railway

---

## Test Commands
Dưới đây là các lệnh bạn dùng trên Terminal để kiểm tra xem hệ thống đã hoạt động đúng chưa.
*(Nhớ thay đoạn URL mẫu thành đường dẫn thật của bạn)*

### Health Check (Kiểm tra hệ thống có sống không)
```bash
curl https://agent-production-0f55.up.railway.app/health
```
**Kết quả kỳ vọng:** `{"status": "ok", "uptime_seconds": ...}`

### API Test (Test bảo mật gửi câu hỏi)
```bash
curl -X POST https://agent-production-0f55.up.railway.app/ask \
  -H "X-API-Key: my-super-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"question": "Xin chào, bạn có hoạt động trên Cloud không?"}'
```

---

## Environment Variables Set
Các biến môi trường đã được cài đặt trên Railway:
- `PORT` (Biến này do hệ thống của Railway tự động cấp để chạy app, không cần thiết lập thủ công)
- `REDIS_URL` (Tự động cấp khi bạn cài đặt tính năng Database Redis trên Railway)
- `AGENT_API_KEY=my-super-secret-key-123`
- `JWT_SECRET=dev-jwt-secret`
- `REDIS_URL` (tự động kết nối từ Redis service của Railway)
- `ENVIRONMENT=production`

---

## Screenshots
*(Vui lòng chụp các ảnh màn hình tương ứng và bỏ vào thư mục `screenshots`)*

- [x] Deployment dashboard (Ảnh chụp màn hình trang quản lý Railway) -> `screenshots/dashboard.png`
- [x] Service running (Ảnh chụp màn hình tab Logs/Console) -> `screenshots/running.png`
- [x] Test results (Ảnh chụp màn hình lúc gọi lệnh Curl báo thành công ở Terminal) -> `screenshots/test.png`
