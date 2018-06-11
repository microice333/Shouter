from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/user/<user_id>", methods=['GET', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        name = redis.get(f"user/{user_id}")
        mail = redis.get(f"user/mail/{user_id}")

        if name:
            return jsonify({'mail': mail.decode('UTF-8'), 'username': name.decode('UTF-8')})
        return jsonify()
    elif request.method == 'PUT':
        name = request.get_json()['name']
        mail = request.get_json()['mail']

        redis.set(f"user/{user_id}", name)
        redis.set(f"user/mail/{user_id}", mail)

        return jsonify({'user_id': user_id})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)