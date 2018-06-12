from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/messages_for/<username>", methods=['GET'])
def all_messages(username):
    messages = []

    for k in redis.keys(pattern='messages/*'):
        author = k.split('/')[1]
        for message in redis.lrange(f"messages/{author}", 0, -1):
            liked = username in redis.smembers(f"likes/{author}/{message}")
            messages.append({'message': message, 'author': author, 'liked': liked})

    return jsonify({'messages': messages})


@app.route("/messages/<username>", methods=['GET', 'PUT'])
def user_messages(username):
    if request.method == 'GET':
        messages = redis.lrange(f"messages/{username}", 0, -1)

        return jsonify({'messages': len(messages)})
    elif request.method == 'PUT':
        message = request.get_json()['message']

        redis.lpush(f"messages/{username}", message)
        messages = redis.lrange(f"messages/{username}", 0, -1)

        return jsonify({'messages': messages})


@app.route("/like/<username>", methods=['PUT', 'DELETE'])
def like(username):
    author = request.get_json()['author']
    message = request.get_json()['message']

    if request.method == 'PUT':
        redis.sadd(f"likes/{author}/{message}", username)

        return jsonify({'message': message, 'author': author, 'liked': True})
    elif request.method == 'DELETE':
        redis.srem(f"likes/{author}/{message}", username)

        return jsonify({'message': message, 'author': author, 'liked': False})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)