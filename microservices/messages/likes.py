import pika
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='message-broker'))
channel = connection.channel()
channel.exchange_declare(exchange='likes',
                         exchange_type='fanout')

queue_name = "likes"
result = channel.queue_declare(exclusive=True, queue=queue_name)
channel.queue_bind(exchange='likes',
                   queue=queue_name)


def callback(ch, method, properties, body):
    idx = body.decode('UTF-8')

    if idx[0] == 'l':
        idx = idx[1:]
        requests.post(f"http://messages:80/likes/{idx}")
    else:
        idx = idx[1:]
        requests.delete(f"http://messages:80/likes/{idx}")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()