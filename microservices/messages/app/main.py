from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/messages/<username>", methods=['GET', 'PUT'])
def user(username):
    if request.method == 'GET':
        messages = redis.lrange(f"messages/{username}", 0, -1)

        if messages:
            return jsonify({'messages': messages})

        return jsonify()
    elif request.method == 'PUT':
        message = request.get_json()['message']

        redis.lpush(f"messages/{username}", message)
        messages = redis.lrange(f"messages/{username}", 0, -1)

        return jsonify({'messages': messages})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)