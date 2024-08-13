import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

ch_2 = connection.channel()

new_queue = ch_2.queue_declare(queue='',
                               exclusive=True)  # set queue to empty make random name for queue like `amq.lksdfo`
# exclusive=True Queue is Auto-Deleted When the Connection Closes

queue_name = new_queue.method.queue

ch_2.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

ch_2.queue_bind(queue=queue_name, exchange='logs')
print('Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f"[x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch_2.basic_consume(
    queue=queue_name,
    on_message_callback=callback
)

ch_2.start_consuming()
