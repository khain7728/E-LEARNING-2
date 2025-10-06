# Client gửi gói với tốc độ cao (chưa tối ưu)

import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005

# Tạo socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet_id = 0 #id thứ tự gói tin
print("Client chưa tối ưu đang gửi gói liên tục... Nhấn Ctrl+C để dừng.")

try:
    start_time = time.time()
    while True:
        send_time = time.time() #Lấy thời điểm bắt đầu gửi tính bằng giâyy
        message = f"{packet_id},{send_time}"  #gộp thành chuỗi "ID, time"
        client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT)) #gửi chuỗi vừa gộp đến server
        packet_id += 1       
except KeyboardInterrupt:
    duration = time.time() - start_time
    print(f"\nĐã gửi {packet_id} gói trong {duration:.2f} giây.")
finally:
    client_socket.close()
    print("Client dừng gửi")