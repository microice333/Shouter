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
        redis.sadd(f"relations/{related_user}", username)
        relations = redis.smembers(f"relations/{username}")

        redis.srem(f"rec-invitations/{username}", related_user)
        redis.srem(f"sent-invitations/{related_user}", username)

        return jsonify({'relations': list(relations)})


@app.route("/sent-invitations/<username>", methods=['PUT', 'GET'])
def sent_invitations(username):
    if request.method == 'PUT':
        invited = request.get_json()['invited']

        redis.sadd(f"sent-invitations/{username}", invited)
        redis.sadd(f"rec-invitations/{invited}", username)
        s_invitations = redis.smembers(f"sent-invitations/{username}")

        return jsonify({'invitations': list(s_invitations)})
    elif request.method == 'GET':
        s_invitations = redis.smembers(f"sent-invitations/{username}")

        return jsonify({'invitations': list(s_invitations)})


@app.route("/received-invitations/<username>", methods=['GET'])
def received_invitations(username):
    invitations = redis.smembers(f"rec-invitations/{username}")

    return jsonify({'invitations': list(invitations)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)