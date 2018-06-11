from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/messages/", methods=['GET'])
def all_messages():
    messages = []

    for k in redis.keys(pattern='messages/*'):
        author = k[len('messages/'):]

        for message in redis.lrange(k, 0, -1):
            messages.append({'message': message, 'author': author})

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)