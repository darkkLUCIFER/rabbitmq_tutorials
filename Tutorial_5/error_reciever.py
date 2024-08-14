import os

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = connection.channel()

ch.exchange_declare(exchange='topic_logs', exchange_type='topic')

queue = ch.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

ch.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='*.*.important')

print('Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    base_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_path, 'error_log.log'), 'a') as f:
        f.write(f"{body.decode("utf-8")}\n")

    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)
ch.start_consuming()
