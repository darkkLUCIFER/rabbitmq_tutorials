import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = connection.channel()

ch.exchange_declare(exchange='topic_logs', exchange_type='topic')

queue = ch.queue_declare(queue='', exclusive=True)
queue_name = queue.method.queue

ch.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='#.not_important')

print('Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode('utf-8')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)

ch.start_consuming()