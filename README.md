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

## Quy trình giao tiếp UDP

### Mô hình hoạt động

```
┌─────────────┐                          ┌─────────────┐
│   CLIENT    │                          │   SERVER    │
└──────┬──────┘                          └──────┬──────┘
       │                                        │
       │ 1. Tạo UDP Socket                      │ 1. Tạo UDP Socket
       │    socket.socket(AF_INET, SOCK_DGRAM)  │    socket.socket(AF_INET, SOCK_DGRAM)
       │                                        │
       │ 2. Cấu hình (nếu optimized)            │ 2. Bind địa chỉ và port
       │    SO_SNDBUF = 65536 (64KB)            │    bind(('127.0.0.1', 5005))
       │    SO_RCVBUF = 65536 (64KB)            │    settimeout(5)
       │                                        │
       │                                        │ 3. Mở file CSV ghi log
       │                                        │    data/results.csv
       │                                        │
       │                                        │ 4. Lắng nghe (recvfrom)
       │                                        │    Chờ nhận dữ liệu (buffer 1024)...
       │                                        │
       │ 3. Gửi gói tin (sendto)                │
       │ ─────────────────────────────────────> │ 5. Nhận gói tin
       │   Format: "{packet_id},{send_time}"    │    receive_time = time.time()
       │   (optimized: ljust(256, b'-'))        │    
       │                                        │ 6. Parse và tính delay
       │                                        │    decoded = data.decode().split(',')
       │                                        │    delay_ms = (receive_time - send_time) * 1000
       │                                        │
       │ 4. Delay (nếu optimized)               │ 7. Ghi vào CSV
       │    time.sleep(1/500) = 0.002s          │    writer.writerow([id, send, recv, delay])
       │                                        │    f.flush()
       │                                        │
       │ 5. Gửi gói tiếp theo (loop)            │ 8. Tiếp tục nhận
       │ ─────────────────────────────────────> │    recvfrom() trong while True
       │                                        │
       │ 6. Hiển thị stats (optimized)          │ 9. Nếu timeout 5s → Break
       │    Mỗi 2s: "Đã gửi X gói"              │    Đóng file CSV
       │                                        │
       │ 7. Kết thúc (Ctrl+C)                   │ 10. Tự động dừng
       │    In tổng số gói đã gửi               │    In "[SERVER] Hết dữ liệu"
       │    Đóng socket                         │    Đóng socket
              └────────────────────────────────────────┘
```

### Chi tiết từng bước

#### **Phía Server (server.py):**

1. **Khởi tạo Socket UDP**
   ```python
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   server_socket.bind(('127.0.0.1', 5005))
   server_socket.settimeout(5.0)  # Timeout 5 giây
   ```

2. **Mở file CSV để ghi log**
   ```python
   with open("data/results.csv", mode="w", newline="", encoding="utf-8") as f:
       writer = csv.writer(f)
       writer.writerow(["packet_id", "send_time", "receive_time", "delay_ms"])
   ```

3. **Nhận và xử lý dữ liệu**
   ```python
   while True:
       data, addr = server_socket.recvfrom(1024)  # Nhận tối đa 1024 bytes
       receive_time = time.time()
       
       # Parse: "packet_id,send_time"
       decoded = data.decode().strip().split(",")
       packet_id = int(decoded[0])
       send_time = float(decoded[1])
       
       # Tính delay (ms)
       delay_ms = (receive_time - send_time) * 1000
       
       # Ghi vào CSV
       writer.writerow([packet_id, send_time, receive_time, round(delay_ms, 3)])
       f.flush()  # Đảm bảo ghi ngay vào file
   ```

4. **Xử lý timeout** - Tự động dừng sau 5s không nhận gói

#### **Phía Client chưa tối ưu (client_unoptimized.py):**

1. **Khởi tạo Socket UDP**
   ```python
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ```

2. **Gửi gói tin liên tục KHÔNG CÓ DELAY**
   ```python
   packet_id = 0
   while True:
       send_time = time.time()
       message = f"{packet_id},{send_time}"
       client_socket.sendto(message.encode(), ('127.0.0.1', 5005))
       packet_id += 1
       # KHÔNG CÓ time.sleep() → Gửi nhanh nhất có thể
   ```

3. **Kết quả**: Tốc độ gửi không kiểm soát → Dễ mất gói, jitter cao

#### **Phía Client đã tối ưu (client_optimized.py):**

1. **Khởi tạo với Buffer lớn**
   ```python
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   # Tăng buffer lên 64KB
   client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
   client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
   ```

2. **Gửi gói tin có kiểm soát tốc độ**
   ```python
   PACKETS_PER_SECOND = 500
   PACKET_SIZE = 256
   interval = 1.0 / PACKETS_PER_SECOND  # 0.002 giây
   
   packet_id = 0
   while True:
       send_time = time.time()
       message = f"{packet_id},{send_time}"
       
       # Padding thành 256 bytes
       data = message.encode().ljust(PACKET_SIZE, b'-')
       
       client_socket.sendto(data, ('127.0.0.1', 5005))
       packet_id += 1
       
       time.sleep(interval)  # Delay giữa các gói = 0.002s
   ```

3. **Hiển thị thống kê real-time**
   ```python
   # Mỗi 2 giây hiển thị progress
   if time.time() - last_display >= 2.0:
       rate = packet_id / elapsed
       print(f"Đã gửi {packet_id} gói ({rate:.1f} gói/giây)")
   ```

4. **Kết quả**: Tốc độ ổn định 500 gói/s, giảm mất gói, jitter thấp

### Đặc điểm giao tiếp UDP

| Đặc điểm | Mô tả |
|----------|-------|
| **Connectionless** | Không cần thiết lập kết nối trước khi gửi |
| **Unreliable** | Không đảm bảo gói tin đến đích |
| **No ordering** | Gói tin có thể đến không đúng thứ tự |
| **Fast** | Overhead thấp, tốc độ cao |
| **Stateless** | Server không lưu trạng thái kết nối |

### So sánh UDP vs TCP

| Tiêu chí | UDP | TCP |
|----------|-----|-----|
| Kết nối | Không cần thiết lập | Cần 3-way handshake |
| Độ tin cậy | Không đảm bảo | Đảm bảo 100% |
| Tốc độ | Nhanh hơn | Chậm hơn |
| Overhead | Thấp (8 bytes header) | Cao (20 bytes header) |
| Use case | Video, gaming, IoT | File transfer, web, email |

## Kiến thức kỹ thuật
```

