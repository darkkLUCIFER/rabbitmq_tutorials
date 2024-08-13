import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

ch_1 = connection.channel()

ch_1.queue_declare(queue='first', durable=True)

message = input('enter message: ')

ch_1.basic_publish(
    exchange='',
    routing_key='first',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # 2 for "persistent", 1 for "transient".
        headers={"name": "amir"},
    )
)
print(f" [x] Sent message {message}")

connection.close()
