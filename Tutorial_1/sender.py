import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

ch_1 = connection.channel()

ch_1.queue_declare(queue='hello')

ch_1.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello World!'
)

print('Message published')

connection.close()
