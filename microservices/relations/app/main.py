from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/relations/<username>", methods=['GET', 'PUT'])
def user(username):
    if request.method == 'GET':
        relations = redis.smembers(f"relations/{username}")

        if relations:
            return jsonify({'relations': list(relations)})

        return jsonify()
    elif request.method == 'PUT':
        related_user = request.get_json()['related_username']

        redis.sadd(f"relations/{username}", related_user)
        relations = redis.smembers(f"relations/{username}")

        return jsonify({'relations': list(relations)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)