import requests
from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/user/<username>", methods=['GET', 'PUT'])
def user(username):
    if request.method == 'GET':
        name = redis.get(f"user/{username}")
        mail = redis.get(f"user/mail/{username}")
        relations = requests.get(f"http://relations:80/relations/{username}").json()
        messages = requests.get(f"http://messages:80/messages/{username}").json()

        if name:
            return jsonify({'mail': mail, 'username': name, **relations, **messages})
        return jsonify()
    elif request.method == 'PUT':
        name = request.get_json()['name']
        mail = request.get_json()['mail']

        redis.set(f"user/{username}", name)
        redis.set(f"user/mail/{username}", mail)

        return jsonify({'user_id': username})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)