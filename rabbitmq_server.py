import socket
import pika
import pickle


server_ip = str(input("Enter broker ip: "))

connection = pika.BlockingConnection(pika.ConnectionParameters(server_ip, 5672, '/', pika.PlainCredentials('datnt621', 'assasint1998')))
channel = connection.channel()

def callback_execution(ch, method, properties, body):
    print(f"Received from client:")
    array = pickle.loads(body)
    print(array)

    choice = array[0]
    array.pop()

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

    print(result)

    channel.basic_publish(exchange='',
                          routing_key='server_respond',
                          body=pickle.dumps(result))

    channel.stop_consuming()
    exit()


channel.queue_declare('client_request')
channel.queue_declare('server_respond')

channel.basic_consume(queue='client_request',
                      auto_ack=True,
                      on_message_callback=callback_execution,)

print("Waiting for client request...")

channel.start_consuming()

