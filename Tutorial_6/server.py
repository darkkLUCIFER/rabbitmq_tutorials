import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = connection.channel()
ch.queue_declare(queue='rpc_queue')

print(' [*] Waiting for messages. To exit press Ctrl+C')


def callback(ch, method, properties, body):
    number = int(body.decode('utf-8'))
    print('Processing message')
    time.sleep(5)

    response = number + 1
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=str(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_qos(prefetch_count=1)
ch.basic_consume(
    queue='rpc_queue',
    on_message_callback=callback
)
ch.start_consuming()
