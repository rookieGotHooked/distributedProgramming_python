import socket
import xmlrpc.server
from datetime import datetime


class OperationsService:
    @staticmethod
    def find_max(array):
        print(f"Received array: {array}")
        print(f"Received at: {datetime.now()}")
        array.sort(reverse=True)
        message = array[0]
        print(f"Message to send: {message}\n")
        return message

    @staticmethod
    def find_min(array):
        print(f"Received array: {array}")
        print(f"Received at: {datetime.now()}")
        array.sort()
        message = array[0]
        print(f"Message to send: {message}\n")
        return message

    @staticmethod
    def find_odds(array):
        print(f"Received array: {array}")
        print(f"Received at: {datetime.now()}")
        odds = []
        for element in array:
            if element % 2 != 0:
                odds.append(element)

        message = odds
        print(f"Message to send: {message}\n")
        return message

    @staticmethod
    def find_evens(array):
        print(f"Received array: {array}")
        print(f"Received at: {datetime.now()}")
        evens = []
        for element in array:
            if element % 2 == 0:
                evens.append(element)

        message = evens
        print(f"Message to send: {message}\n")
        return message

    @staticmethod
    def find_primes(array):
        print(f"Received array: {array}")
        print(f"Received at: {datetime.now()}")
        primes = []

        for element in array:
            if element <= 1:
                continue
            else:
                flag_is_prime = False
                for i in range(2, int(element ** 0.5) + 1):
                    if element % i == 0:
                        flag_is_prime = True
                        break
                if not flag_is_prime:
                    primes.append(element)

        message = primes
        print(f"Message to send: {message}\n")
        return message

    @staticmethod
    def handshake():
        return True

    @staticmethod
    def get_server_ip():
        return server_ip

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

server = xmlrpc.server.SimpleXMLRPCServer((server_ip, 8000))
server.register_instance(OperationsService())
print(f"Listening on {server_ip}:8000...")
server.serve_forever()
