import atexit
import socket
import threading
from datetime import datetime


# Hàm xử lý đóng kết nối khi ngắt chương trình
def exit_handler():
    server_socket.close()
    print("Socket closed")


# Hàm chuyển đổi chuỗi sang list các phần tử
def convert_str_to_list(array_string):
    return [int(elem) for elem in array_string.split()]


# Hàm tìm các phần tử chẵn trong mảng nhận được và trả về dưới dạng chuỗi
def list_evens(arr):
    evens = []

    for elem in arr:
        if elem % 2 == 0:
            evens.append(str(elem))

    evens_string = " ".join(evens)
    print(f"Evens elements within the array are: {evens_string}")
    print(f"Executed at {datetime.now()} on server")
    return evens_string


# Hàm tìm các phần tử lẻ trong mảng nhận được và trả về dưới dạng chuỗi
def list_odds(arr):
    odds = []

    for elem in arr:
        if elem % 2 != 0:
            odds.append(str(elem))

    odds_string = " ".join(odds)
    print(f"Odds elements within the array are: {odds_string}")
    print(f"Executed at {datetime.now()} on server")
    return odds_string


# Hàm xử lý mỗi khi nhận được kết nối từ client
def on_connection(connection, address):
    print(f"Received connection from {address}")

    # Nhận dữ liệu từ client - là mảng toàn cục
    data = connection.recv(1024).decode()
    print(f"Received message: {data}")

    # Xử lý dữ liệu và chuyển về dạng list
    print(f"Converting string data to list...")
    processed_data = convert_str_to_list(data)
    print(f"processed_data = {processed_data}")

    # Chạy 2 hàm tìm chẵn / lẻ trong mảng toàn cục
    print(f"Executing array...")
    respond_evens = list_evens(processed_data)
    respond_odds = list_odds(processed_data)

    # Hiển thị kết quả đã chạy (đồng thời là thông điệp sẽ gửi cho client)
    print("Message to send to client:")
    print(f"respond_evens: {respond_evens}")
    print(f"respond_odds: {respond_odds}")

    # Gửi 2 thông điệp - list chứa các phần tử chẵn / lẻ; các thông điệp được gửi đi sẽ bị mã hóa
    print("Attempting to send message...")
    connection.send(respond_evens.encode())
    connection.send(respond_odds.encode())

    # In ra thời gina hoàn thành
    print("Completed!")
    print(f"Thread end at {datetime.now()}\n")


# Biến quy định số lượng kết nối cùng lúc (từ client tới server)
threads = 3

# Thực hiện kết nối tới DNS của Google (8.8.8.8) và lấy IP, sau đó đóng cổng
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

# Tạo kết nối socket cho luồng dữ liệu và gán vào cổng 8000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, 8000))

# Quy định số lượng kết nối cùng lúc
server_socket.listen(threads)

# In ra rằng server đang đợi kết nối trên cổng 8000
print(f"Server listening on {server_ip}: 8000")

# Gắn hàm xử lý khi thoát chương trình
atexit.register(exit_handler)

# Lặp vô hạn:
while True:
    # Đợi kết nối từ client
    conn, addr = server_socket.accept()

    # Khi nhận được kết nối, tạo luồng mới và xử lý hàm on_connection
    thread = threading.Thread(on_connection(conn, addr, ))
    thread.start()

    # Note: Không cần dùng semaphore hay monitor bởi chính socket đã giới hạn số lượng kết nối cùng lúc
