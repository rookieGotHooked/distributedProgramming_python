import pika
import socket
import random
import pickle
from datetime import datetime
import uuid


def generate_array(count=10):
    array = []

    while len(array) < count:
        array.append(random.randint(1, 100))

    return array


def display_result(ch, method, properties, body):
    result = pickle.loads(body)
    result.pop(0)
    print(f"Result ID: {result[0]}")
    print(f"Request result: {result[1]}")


def record(ch, method, properties, body):
    new_message = pickle.loads(body)

    msg_type = new_message.pop(0)
    msg_id = new_message.pop(0)

    if msg_type == message_type[0]:
        rqs_type = new_message[0]
        new_message.pop(0)

        if rqs_type == 1:
            translated_rqs_type = "max"
        elif rqs_type == 2:
            translated_rqs_type = "min"
        elif rqs_type == 3:
            translated_rqs_type = "prime"
        else:
            raise Exception("Invalid request type received when recording messages")

        request_log.append((msg_id, translated_rqs_type, new_message, datetime.now()))
        display_request_log()
    elif msg_type == message_type[1]:
        respond_log.append((msg_id, new_message, datetime.now()))
        display_respond_log()
    else:
        raise Exception("Invalid message type received when recording messages")


def display_request_log():
    print("Current request log:")
    for log in request_log:
        print(log)

def display_respond_log():
    print("Current respond log:")
    for log in respond_log:
        print(log)


def server_handle_request(ch, method, properties, body):
    print(f"Received from client:")
    array = pickle.loads(body)
    print(array)

    array.pop(0)
    request_id = array.pop(0)
    choice = array.pop(0)

    if choice == 1:
        array.sort(reverse=True)
        result = array[0]
    elif choice == 2:
        array.sort()
        result = array[0]
    elif choice == 3:
        result = []

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
                    result.append(element)
    else:
        raise Exception("")

    final_result = [message_type[1], request_id, result]
    print(f"Result to send: {final_result}")

    channel.basic_publish(exchange=exchange,
                          routing_key=task_types[1],
                          body=pickle.dumps(final_result))

    channel.basic_publish(exchange=exchange,
                          routing_key=task_types[2],
                          body=pickle.dumps(final_result))

    channel.stop_consuming()
    exit()


exchange = 'tasks_exchange'
task_types = ["tasks.request", "tasks.respond", "tasks.record"]

server_ip = str(input("Enter broker ip: "))

message_type = ["request", "respond"]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(server_ip, 5672, '/', pika.PlainCredentials('datnt621', 'assasint1998')))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')


print("Enter role:")
print("1. Server")
print("2. Client (request)")
print("3. Client (record)")
role_choice = int(input("Enter role choice: "))

if role_choice == 1:
    queue_declare = channel.queue_declare(queue='task_request')
    queue_name_request = queue_declare.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name_request, routing_key=task_types[0])

    queue_declare = channel.queue_declare(queue='task_respond')
    queue_name_respond = queue_declare.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name_respond, routing_key=task_types[1])

    queue_declare = channel.queue_declare(queue='task_record')
    queue_name_record = queue_declare.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name_record, routing_key=task_types[2])

    channel.basic_consume(queue=queue_name_request,
                          auto_ack=True,
                          on_message_callback=server_handle_request, )

    print("Waiting for client request...")

    channel.start_consuming()

elif role_choice == 2:
    print("Send request for...?")
    print("1. Find Max element of the array")
    print("2. Find Min element of the array")
    print("3. Find all prime element of the array")
    request_choice = int(input("Enter request choice: "))

    new_request_id = str(uuid.uuid4())

    arrayA = [message_type[0], new_request_id, request_choice]
    arrayA.extend(generate_array(10))

    channel.basic_publish(exchange=exchange,
                          routing_key=task_types[0],
                          body=pickle.dumps(arrayA))

    channel.basic_publish(exchange=exchange,
                          routing_key=task_types[2],
                          body=pickle.dumps(arrayA))

    print(f'Sending array request: {arrayA}')

    queue_declare = channel.queue_declare(queue='task_respond')
    queue_name = queue_declare.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=task_types[1])

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=display_result)

    channel.start_consuming()

elif role_choice == 3:
    request_log = []
    respond_log = []

    queue_declare = channel.queue_declare(queue='task_record')
    queue_name = queue_declare.method.queue
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=task_types[2])

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=record)

    print("Waiting for new message...")
    channel.start_consuming()
else:
    raise Exception("Unexpected role choice received")