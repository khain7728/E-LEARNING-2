# E-LEARNING-2: UDP Performance Optimization Demo

## Mô tả dự án

Ứng dụng mô phỏng và so sánh hiệu suất UDP trước và sau khi tối ưu hóa bằng cách:
- **Tăng kích thước bộ đệm (buffer)** để giảm mất gói
- **Điều chỉnh tốc độ gửi** để tránh nghẽn mạng
- **Phân tích và so sánh** độ trễ, jitter và tỷ lệ mất gói

## Mục tiêu so sánh

| Tiêu chí | Trước khi tối ưu | Sau khi tối ưu |
|----------|------------------|----------------|
| **Tốc độ truyền** | Gửi gói liên tục tốc độ cao → dễ nghẽn | Gửi theo tốc độ tối ưu (500 gói/s) |
| **Tỷ lệ mất gói** | Cao do buffer đầy | Giảm đáng kể nhờ buffer lớn |
| **Độ trễ trung bình** | Không ổn định, có jitter cao | Ổn định hơn, jitter thấp |
| **Hiệu năng** | Không kiểm soát → lãng phí băng thông | Sử dụng băng thông hiệu quả |

## Cấu trúc dự án

```
E-LEARNING-2/
├── Client/
│   ├── client_unoptimized.py    # Client gửi gói tốc độ cao (chưa tối ưu)
│   └── client_optimized.py      # Client gửi gói có điều chỉnh tốc độ + buffer
├── Server/
│   ├── server.py                # Server nhận gói, đo độ trễ, ghi log
│   └── data/                    # Thư mục chứa dữ liệu server
├── Data/
│   ├── results.csv              # Kết quả client chưa tối ưu
│   └── results_optimized.csv    # Kết quả client đã tối ưu
├── Analysis/
│   ├── analyze_results.py       # Phân tích và vẽ biểu đồ so sánh
│   ├── metrics_comparison.csv   # Bảng so sánh metrics
│   ├── udp_delay_comparison.png # Biểu đồ so sánh
│   └── udp_optimization_report.txt # Báo cáo chi tiết
└── README.md                    # File này
```

## Các chức năng đã implement

✅ **Server (server.py)**
- Tạo socket UDP nhận gói từ client
- Đo thời gian nhận để tính độ trễ
- Ghi log vào file CSV với format: packet_id, send_time, receive_time, delay_ms
- Timeout 5s để tự động dừng khi hết dữ liệu

✅ **Client chưa tối ưu (client_unoptimized.py)**
- Gửi gói liên tục với tốc độ tối đa (không có delay)
- Mô phỏng tình trạng mất gói và jitter cao
- Gói tin nhỏ, không kiểm soát tốc độ

✅ **Client đã tối ưu (client_optimized.py)**
- Điều chỉnh tốc độ gửi: 500 gói/giây với `time.sleep()`
- Tăng buffer size: 64KB cho send và receive buffer
- Gói tin cố định 256 bytes
- Hiển thị thống kê real-time mỗi 2 giây

✅ **Phân tích dữ liệu (analyze_results.py)**
- So sánh metrics: delay trung bình, max, jitter, percentile 95/99
- Tính tỷ lệ mất gói dựa trên khoảng trống packet_id
- Vẽ biểu đồ matplotlib: line chart, histogram, boxplot, bar chart
- Xuất báo cáo text và CSV

## Cách chạy dự án

### Bước 1: Cài đặt dependencies

```bash
# Cài đặt matplotlib để vẽ biểu đồ
pip install matplotlib numpy
```

### Bước 2: Chạy thử nghiệm client chưa tối ưu

**Terminal 1 - Khởi động Server:**
```bash
cd Server
python server.py
```
Server sẽ hiển thị: `[SERVER] Listening on 127.0.0.1:5005`

**Terminal 2 - Chạy Client chưa tối ưu:**
```bash
cd Client  
python client_unoptimized.py
```
Để dừng client, nhấn `Ctrl+C`. Server sẽ tự động dừng sau 5s không nhận gói.

### Bước 3: Chạy thử nghiệm client đã tối ưu

**Terminal 1 - Khởi động lại Server:**
```bash
cd Server
python server.py
```

**Terminal 2 - Chạy Client đã tối ưu:**
```bash
cd Client
python client_optimized.py  
```
Client sẽ hiển thị thống kê real-time. Nhấn `Ctrl+C` để dừng.

### Bước 4: Phân tích kết quả

```bash
cd Analysis
python analyze_results.py
```

Kết quả sẽ tạo ra:
- **udp_delay_comparison.png**: Biểu đồ so sánh 4 góc độ
- **udp_optimization_report.txt**: Báo cáo chi tiết  
- **metrics_comparison.csv**: Bảng số liệu so sánh

## Kết quả mong đợi

Sau khi chạy thử nghiệm, bạn sẽ thấy sự cải thiện rõ rệt:

| Metric | Client chưa tối ưu | Client đã tối ưu | Cải thiện |
|--------|-------------------|------------------|-----------|
| **Delay trung bình** | ~400-500ms | ~200-300ms | 30-40% |
| **Jitter trung bình** | Cao, không ổn định | Thấp, ổn định | 40-60% |
| **Tỷ lệ mất gói** | 5-15% | 1-3% | 70-80% |
| **Độ ổn định** | Biến động lớn | Ổn định cao | Tốt hơn rõ rệt |

## Kiến thức kỹ thuật

### Tối ưu hóa được áp dụng:

1. **Buffer Size**: Tăng từ default (~8KB) lên 64KB
   ```python
   client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
   client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
   ```

2. **Rate Limiting**: Kiểm soát tốc độ gửi 500 gói/giây
   ```python
   interval = 1.0 / PACKETS_PER_SECOND  # 0.002s giữa các gói
   time.sleep(interval)
   ```

3. **Fixed Packet Size**: Gói tin cố định 256 bytes để dễ phân tích
   ```python
   data = message.encode().ljust(PACKET_SIZE, b'-')
   ```

### Metrics được đo:
- **Delay**: Thời gian từ lúc gửi đến lúc nhận (ms)
- **Jitter**: Độ biến thiên delay giữa các gói liên tiếp  
- **Packet Loss**: Tỷ lệ gói bị mất dựa trên gap trong packet_id
- **Percentile 95/99**: Delay của 95% và 99% gói tốt nhất

## Nhóm phát triển

- **Nguyễn Quốc Khải**: Server + logging system ✅
- **Lê Viết Sang**: Client unoptimized ✅  
- **Nguyễn Thị Thùy Trang**: Client optimized ✅
- **Nguyễn Đỗ Anh Khoa**: Data analysis + visualization ✅
- **Huỳnh Thị Quý Trân**: Documentation + testing ✅

## Lưu ý khi chạy

1. **Chạy Server trước Client**: Server phải khởi động trước khi client gửi gói
2. **Dữ liệu ghi đè**: Mỗi lần chạy server sẽ tạo file CSV mới
3. **Cần Python 3.7+**: Để đảm bảo tương thích với các thư viện
4. **Firewall**: Đảm bảo port 5005 không bị chặn
5. **Performance**: Chạy trên localhost để kết quả chính xác nhất

## Mở rộng có thể

- Thêm nhiều client đồng thời
- Test với network conditions khác nhau (latency, packet loss)  
- Thử nghiệm với UDP multicast
- Implement TCP comparison
- Real-time monitoring dashboard