import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

ch_1 = connection.channel()

ch_1.queue_declare(queue='hello')

ch_1.exchange_declare(
    exchange='logs',  # name of the exchange
    exchange_type='fanout',
)

ch_1.basic_publish(
    exchange='logs',
    routing_key='',
    body='this is testing fanout',
)

print('sent message')
connection.close()
