import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

ch_2 = connection.channel()

ch_2.queue_declare(queue='first', durable=True)
print('Waiting for messages. To exit press Ctrl+C')


def callback(ch, method, properties, body):
    print(f"[x] Received {body.decode('utf-8')}")
    print(f"[x] Receiver name: {properties.headers['name']}")
    time.sleep(10)
    print("[x] Done")
    print(method)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # send ack after process is done


ch_2.basic_qos(prefetch_count=1)  # send one message for each consumer
ch_2.basic_consume(
    queue='first',
    on_message_callback=callback
)

ch_2.start_consuming()
