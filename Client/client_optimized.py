# Client gửi gói có điều chỉnh tốc độ + buffer

import socket  # Dùng để tạo và thao tác với socket UDP
import time    # Dùng để đo thời gian, tính tốc độ, giới hạn tốc độ gửi

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

# Cấu hình hiệu suất
SEND_BUFFER_SIZE = 65536      # 64 KB buffer gửi
RECV_BUFFER_SIZE = 65536      # 64 KB buffer nhận (nếu cần)
PACKETS_PER_SECOND = 500      # tốc độ gửi (500 gói/giây)
PACKET_SIZE = 256             # độ dài mỗi gói (byte)
DISPLAY_INTERVAL = 2          # in thống kê mỗi 2 giây

# Tạo socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# AF_INET: dùng IPv4
# SOCK_DGRAM: dùng giao thức UDP (gửi theo datagram, không đảm bảo thứ tự hay độ tin cậy)

# Điều chỉnh buffer
# Buffer lớn giúp tránh mất gói khi tốc độ gửi cao hoặc mạng trễ
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUFFER_SIZE)

print(f"Client đang gửi với tốc độ {PACKETS_PER_SECOND} gói/giây, mỗi gói {PACKET_SIZE} bytes.")
print("Nhấn Ctrl+C để dừng...")

packet_id = 0                     # Số thứ tự gói gửi đi
start_time = time.time()          # Thời điểm bắt đầu gửi
last_display = start_time         # Thời điểm lần cuối in thống kê


# Khoảng trễ giữa 2 gói để đạt tốc độ mong muốn
interval = 1.0 / PACKETS_PER_SECOND   # VD: 500 gói/giây → mỗi gói cách nhau 0.002 giây
try:
    while True:
        # Ghi lại thời điểm gửi
        send_time = time.time()

        # Tạo nội dung gói tin gồm ID và thời gian gửi
        message = f"{packet_id},{send_time}"

        # Chuyển chuỗi sang bytes, và pad thêm ký tự '-' để đủ PACKET_SIZE byte
        # (Giúp server dễ xử lý gói có kích thước cố định)
        data = message.encode().ljust(PACKET_SIZE, b'-')
        
        # Gửi gói tin UDP tới server
        client_socket.sendto(data, (SERVER_IP, SERVER_PORT))

        # Tăng ID cho gói kế tiếp
        packet_id += 1

        # Giới hạn tốc độ gửi
        time.sleep(interval) # Dừng lại trong 'interval' giây để đảm bảo đúng tốc độ mong muốn

        now = time.time()
        if now - last_display >= DISPLAY_INTERVAL:
            elapsed = now - start_time                 # Tổng thời gian chạy
            rate = packet_id / elapsed                 # Tính tốc độ trung bình (gói/giây)
            print(f" Đã gửi {packet_id} gói ({rate:.1f} gói/giây)")
            last_display = now                         # Cập nhật mốc hiển thị mới

except KeyboardInterrupt:
    duration = time.time() - start_time
    print(f"\n Đã gửi {packet_id} gói trong {duration:.2f} giây.")

finally:
    client_socket.close()
    print("Client dừng gửi.")