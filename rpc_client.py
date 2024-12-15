import xmlrpc.client
import random


def generate_array(count):
    generated_array = []

    while len(generated_array) < count:
        generated_array.append(random.randint(0, 100))

    return generated_array


array = generate_array(10)

print("Choose one of the below methods:")
print("1. Return Max element of an integer array")
print("2. Return Min element of an integer array")
print("3. Return Odd elements of an integer array")
print("4. Return Even elements of an integer array")
print("5. Return Prime elements of an integer array\n")

choice = 0

while choice not in range(1, 5):
    choice = int(input("Pick a method (1-5):"))

# server_ip = input("Enter server ip:")
server_ip = "192.168.155.96"

try:
    with xmlrpc.client.ServerProxy(f"http://{server_ip}:8000/") as proxy:
        if proxy.handshake():
            print(f"\nConnected to server: {proxy.get_server_ip}")
except e:
    print(f"\nEncountered error: {e}")
    exit()

print(f"Generated array: {array}")

if choice == 1:
    print(f"Max element of array: {proxy.find_max(array)}")
elif choice == 2:
    print(f"Min element of array: {proxy.find_min(array)}")
elif choice == 3:
    print(f"Odd elements of array: {proxy.find_odds(array)}")
elif choice == 4:
    print(f"Even elements of array: {proxy.find_evens(array)}")
elif choice == 5:
    print(f"Prime elements of array: {proxy.find_primes(array)}")
