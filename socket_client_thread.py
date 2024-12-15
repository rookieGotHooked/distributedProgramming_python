import atexit
import socket
import random
import time
from datetime import datetime


# Hàm xử lý đóng kết nối khi ngắt chương trình
def exit_handler():
    client_socket.close()
    print("Socket closed")


# Hàm chuyển đổi chuỗi sang list các phần tử
def convert_str_to_list(array_string):
    return [int(elem) for elem in array_string.split()]


# Tạo mảng các phần tử mới và chuyển sang dạng string (cách nhau bằng dấu cách)
def generate_array():
    a = []

    while len(a) < 200:
        a.append(str(random.randint(0, 100)))

    str_a = " ".join(a)
    return str_a


# Hàm hiển thị kết quả đầu ra
def display_result(evens, evens_time, odds, odds_time):
    print(f"Evens elements in the array are: {convert_str_to_list(evens)}")
    print(f"Time received: {evens_time}")
    print(f"Evens elements in the array are: {convert_str_to_list(odds)}")
    print(f"Time received: {odds_time}")


# Gắn hàm xử lý khi thoát chương trình
atexit.register(exit_handler)

while True:
    # Thực hiện kết nối với địa chỉ IP public của server (có thể tìm địa chỉ này trên Google)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.47', 8000))

    # Tạo mảng và convert sang dạng chuỗi thông điệp
    print("Generating message")
    message = generate_array()
    print(f"Generated message: {message}")

    # Mã hóa thông điệp và gửi thông điệp tới server
    print("Attempting to send message...")
    client_socket.send(message.encode())

    # Nhận thông điệp từ server:
    # Nhận thông điệp các phần tử chẵn từ server
    received_evens = client_socket.recv(1024).decode()
    received_evens_time = datetime.now()

    # Nhận thông điệp các phần tử lẻ từ server
    received_odds = client_socket.recv(1024).decode()
    received_odds_time = datetime.now()

    # Hiển thị thông điệp
    print("Received messages:")
    display_result(received_evens, received_evens_time, received_odds, received_odds_time)

    # Mỗi 2s lại bắt đầu kết nối và lặp lại vòng lặp while
    time.sleep(2)
