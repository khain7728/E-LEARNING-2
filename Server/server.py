# Server nhận gói, đo độ trễ, đếm gói
import socket
import csv
import os
import time

HOST = "127.0.0.1"
PORT = 5005
DATA_FILE = os.path.join("data", "results.csv")

# Tạo thư mục data nếu chưa có
os.makedirs("data", exist_ok=True)

# Tạo socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    # Mở file CSV để ghi kết quả
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["packet_id", "send_time", "receive_time", "delay_ms"])

        s.settimeout(5)  # Dừng server nếu không nhận thêm gói nào sau 5s

        while True:
            try:
                data, addr = s.recvfrom(1024)
                receive_time = time.time()

                decoded = data.decode().strip().split(",")
                packet_id = int(decoded[0])
                send_time = float(decoded[1])
                delay_ms = (receive_time - send_time) * 1000

                print(f"[RECV] Gói {packet_id} từ {addr} | Độ trễ: {delay_ms:.2f} ms")

                # Ghi log vào CSV
                writer.writerow([packet_id, send_time, receive_time, round(delay_ms, 3)])
                f.flush()

            except socket.timeout:
                print("\n[SERVER] Hết dữ liệu, kết thúc ghi log.")
                break
            except Exception as e:
                print(f"[LỖI] {e}")
