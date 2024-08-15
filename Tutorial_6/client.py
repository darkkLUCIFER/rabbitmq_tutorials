import pika
import uuid


class Client:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.ch = self.connection.channel()
        queue = self.ch.queue_declare(queue='', exclusive=True)
        self.queue_name = queue.method.queue
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.ch.basic_consume(queue=self.queue_name, on_message_callback=self.on_response_callback, auto_ack=True)

    @staticmethod
    def get_instance():
        return Client()

    def call(self, number: int):
        self.ch.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.queue_name,
                correlation_id=self.correlation_id,
            ),
            body=str(number)
        )
        while self.response is None:
            # wait to process done
            self.connection.process_data_events()

        return int(self.response)

    def on_response_callback(self, ch, method, properties, body):
        if self.correlation_id == properties.correlation_id:
            self.response = body


client = Client.get_instance()
response = client.call(30)
print(response)
