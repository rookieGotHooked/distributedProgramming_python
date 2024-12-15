import threading
import random
import time
from datetime import datetime


# Các mảng:
arrayA = []             # mảng toàn cục
read_threads = []       # mảng các luồng đọc
write_threads = []      # mảng các luồng viết

# Các biến kiểm tra / biến cờ (flags)
# Note: nếu kiểm tra số nguyên tố đặt là true, biến còn lại phải đặt là false (và ngược lại)
is_check_prime = False  # kiểm tra số nguyên tố
is_check_even = True    # kiểm tra số chẵn lẻ

# Semaphore: Giới hạn số lượng luồng chạy cùng lúc theo biến đếm
single_semaphore = threading.Semaphore(1)


# Hàm thêm số nguyên ngẫu nhiên (trong khoảng 0 - 1000) vào mảng arrayA, dựa theo số lượng đầu vào
def add_element(element_count):
    count = 0
    while count < element_count:
        arrayA.append(random.randint(0, 1000))
        count += 1


# Hàm tạo các luồng đọc, dựa theo số lượng luồng đầu vào
# Mỗi luồng được gán với hàm read_thread
def create_read_threads(thread_count):
    count = 0
    while count < thread_count:
        thread = threading.Thread(target=read_thread, args=(count, ))
        read_threads.append(thread)
        count += 1


# Hàm tạo các luồng viết, dựa theo số lượng luồng đầu vào
# Mỗi luồng được gán với hàm write_thread
def create_write_threads(thread_count):
    count = 0
    while count < thread_count:
        thread = threading.Thread(target=write_thread, args=(count, ))
        write_threads.append(thread)
        count += 1


# Hàm xử lý luồng đọc dựa theo thứ tự luồng
def read_thread(thread_index):
    # Tương ứng với semaphore.aquire() - "lấy" quyền truy cập dựa theo semaphore đếm;
    # nếu biến đếm semaphore > 1 thì luồng được chạy
    with single_semaphore:

        # Xử lý nếu mảng A rỗng
        if len(arrayA) == 0:
            # Thông báo mảng A rỗng tại thời điểm hiện tại
            print(f"R-{thread_index}: arrayA is empty ; {datetime.now()}")

        # Nếu mảng A không rỗng
        else:
            # Lấy phần tử ngẫu nhiên trong arrayA
            random_index = random.randint(0, len(arrayA) - 1)
            temp = arrayA[random_index]
            del arrayA[random_index]

            # Nếu chọn kiểm tra số lấy ra khỏi arrayA là số nguyên tố (hay không):
            if is_check_prime:
                if check_prime(temp):
                    print(f"R-{thread_index}: {temp} : prime ; {datetime.now()}")
                else:
                    print(f"R-{thread_index}: {temp} : not prime ; {datetime.now()}")

            # Nếu chọn kiểm tra số lấy ra khỏi arrayA là số chắn (hay lẻ):
            elif is_check_even:
                if check_even(temp):
                    print(f"R-{thread_index}: {temp} : even ; {datetime.now()}")
                else:
                    print(f"R-{thread_index}: {temp} : odd ; {datetime.now()}")

            # Cho luồng hiện tại tạm dừng trong khoảng ngẫu nhiên từ 1s - 5s
            random_sleep = random.randint(1, 5)
            print(f"R-{thread_index} sleeping for {random_sleep} second(s)\n")
            time.sleep(random_sleep)


# Hàm kiểm tra số nguyên tố
def check_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True


# Hàm kiểm tra số chẵn - lẻ
def check_even(n):
    return n % 2 == 0


# Hàm xử lý luồng viết theo thứ tự luồng
def write_thread(thread_index):
    with single_semaphore:
        # Thêm số nguyên ngẫu nhiên trong khoảng 0-1000 vào arrayA
        random_int = random.randint(0, 1000)
        arrayA.append(random_int)

        # In số vừa thêm
        print(f"W-{thread_index}: {random_int}; {datetime.now()}")

        # Cho luồng hiện tại tạm dừng ngẫu nhiên trong khoảng 1s - 5s
        random_sleep = random.randint(1, 5)
        print(f"W-{thread_index} sleeping for {random_sleep} second(s)\n")
        time.sleep(random_sleep)


# Bắt đầu các luồng viết đã được lưu trong mảng write_threads
def start_write_threads():
    for thread in write_threads:
        thread.start()


# Bắt đầu các luồng đọc đã được lưu trong mảng read_threads
def start_read_threads():
    for thread in read_threads:
        thread.start()


# Phần chạy chương trình chính:
# Nhập số luồng đọc
print("Enter the number of write threads:")
write_count = int(input("write_count = "))

# Nhập số luồng viết
print("Enter the number of read threads:")
read_count = int(input("read_count = "))

# Tạo các luồng đọc / viết dựa theo số lượng đã nhập
create_write_threads(write_count)
create_read_threads(read_count)

# Chạy lệnh liên tục không dừng:
while True:
    # Loại bỏ tất cả các luồng đọc / viết đã lưu
    write_threads.clear()
    read_threads.clear()

    # Tạo các luồng đọc / viết + lưu vào các mảng write_threads và read_threads
    create_write_threads(write_count)
    create_read_threads(read_count)

    # Bắt đầu các luồng đọc / viết
    start_write_threads()
    start_read_threads()

    # Tạm dừng chương trình trong 2s sau khi hoàn thành việc bắt đầu các luồng
    time.sleep(2)
