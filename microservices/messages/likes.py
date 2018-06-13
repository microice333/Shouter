import pika
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='message-broker'))
channel = connection.channel()
channel.exchange_declare(exchange='likes',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = "likes"
channel.queue_bind(exchange='likes',
                   queue=queue_name)


def callback(ch, method, properties, body):
    idx = body.decode('UTF-8')
    requests.put(f"http://messages:80/likes/{idx}")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()