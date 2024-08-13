import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch2 = connection.channel()
ch2.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


ch2.basic_consume(
    queue='hello',
    auto_ack=True,
    on_message_callback=callback
)

print('waiting for message, to exit press ctrl+c')

ch2.start_consuming()
