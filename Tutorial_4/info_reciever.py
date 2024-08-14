import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

ch = connection.channel()

ch.exchange_declare(exchange='direct_logs', exchange_type='direct')

queue = ch.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

severities = ('info', 'warning', 'error')

for severity in severities:
    ch.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print('Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f'{method.routing_key}: {body.decode("utf-8")}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)

ch.start_consuming()
