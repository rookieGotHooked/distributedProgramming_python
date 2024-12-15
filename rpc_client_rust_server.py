import xmlrpc.client
import random
from message_protobuf_pb2 import GreetMessage


def generate_array(count):
    generated_array = []

    while len(generated_array) < count:
        generated_array.append(random.randint(0, 100))

    return generated_array


array = generate_array(10)

# server_ip = input("Enter server ip:")
# server_ip = "192.168.155.96"
server_ip = "192.168.176.111"

try:
    with xmlrpc.client.ServerProxy(f"http://{server_ip}:8000") as proxy:
        print(proxy.count_prime)
        # name = {'name': "Dat"}
        # message = GreetMessage(name="Dat")
        # proxy.say_hello(message)
        count = proxy.count_prime(array)
        print(f"Generated count: {count}")
            # proxy.count_prime(array)
except e:
    print(f"\nEncountered error: {e}")
    exit()


