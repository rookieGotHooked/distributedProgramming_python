import pika
import socket
import random
import pickle


def generate_array(count = 10):
    array = []

    while len(array) < count:
        array.append(random.randint(1, 100))

    return array


server_ip = str(input("Enter broker ip: "))
print("Send request for...?")
print("1. Find Max element of the array")
print("2. Find Min element of the array")
print("3. Find all prime element of the array")
choice = int(input("Enter request choice:"))

arrayA = [choice]
arrayA.extend(generate_array(10))

connection = pika.BlockingConnection(pika.ConnectionParameters(server_ip, 5672, '/', pika.PlainCredentials('datnt621', 'assasint1998')))
channel = connection.channel()

channel.queue_declare('client_request')
channel.queue_declare('server_respond')

channel.basic_publish(exchange='',
                      routing_key='client_request',
                      body=pickle.dumps(arrayA))

print(f'Sending array: {arrayA}')


def display_result(ch, method, properties, body):
    result = pickle.loads(body)
    print(f"Received result: {result}")


channel.basic_consume(queue='server_respond',
                      auto_ack=True,
                      on_message_callback=display_result)

channel.start_consuming()
