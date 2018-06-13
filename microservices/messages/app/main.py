import requests
from flask import Flask, jsonify, request
from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2, charset="utf-8", decode_responses=True)

app = Flask(__name__)


@app.route("/messages_for/<username>", methods=['GET'])
def all_messages(username):
    messages = []

    relations = requests.get(f"http://relations:80/relations/{username}").json()
    if 'relations' in relations.keys():
        relations = relations['relations']
    else:
        relations = []

    relations.append(username)

    for k in redis.keys(pattern='messages_u/*'):
        author = k.split('/')[1]

        if not author in relations:
            for idx in redis.lrange(f"messages_u/{author}", 0, -1):
                liked = username in redis.smembers(f"likes/{idx}")
                message = redis.get(f"messages/{idx}")
                messages.append({'message': message, 'author': author, 'liked': liked, 'id': idx})

    return jsonify({'messages': messages})


@app.route("/messages/<username>", methods=['GET', 'PUT'])
def user_messages(username):
    if request.method == 'GET':
        messages = redis.lrange(f"messages_u/{username}", 0, -1)

        return jsonify({'messages': len(messages)})
    elif request.method == 'PUT':
        message = request.get_json()['message']
        idx = redis.incr("messages/id")
        redis.lpush(f"messages_u/{username}", idx)
        redis.set(f"messages/{idx}", message)
        redis.set(f"authors/{idx}", username)

        return jsonify({'id': idx})


@app.route("/like/<username>", methods=['PUT', 'DELETE'])
def like(username):
    idx = request.get_json()['idx']

    if request.method == 'PUT':
        redis.sadd(f"likes/{idx}", username)
        message = redis.get(f"messages/{idx}")
        author = redis.get(f"authors/{idx}")

        return jsonify({'message': message, 'author': author, 'liked': True, 'id': idx})
    elif request.method == 'DELETE':
        redis.srem(f"likes/{idx}", username)
        message = redis.get(f"messages/{idx}")
        author = redis.get(f"authors/{idx}")

        return jsonify({'message': message, 'author': author, 'liked': False, 'id': idx})


@app.route("/likes/<idx>", methods=['POST', 'GET', 'DELETE'])
def likes(idx):
    if request.method == 'POST':
        author = redis.get(f"authors/{idx}")
        redis.incr(f"likes/{author}")

        return jsonify({})
    elif request.method == 'DELETE':
        author = redis.get(f"authors/{idx}")
        redis.decr(f"likes/{author}")

        return jsonify({})
    elif request.method == 'GET':
        return jsonify({'likes': redis.get(f"likes/{idx}")})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
