from flask import request, jsonify, session
from flask.views import MethodView
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from ...models.model import count_user,count_album,count_songs



def stats_count():
    if request.method == 'GET':
        role = request.args.get('role')
        print(role)
        count = count_user(role)
        if count is None:
            return jsonify('{error: count is not called properly}') ,400
        return jsonify(count),200

def stats_album_count():
    count = count_album()
    if count is None:
        return jsonify('{error: count is not called properly}') ,400
    return jsonify(count),200


def stats_songs_count():
    count = count_songs()
    if count is None:
        return jsonify('{error: count is not called properly}') ,400
    return jsonify(count),200

def stats_total():
    count_c = count_user('creator')
    count_u = count_user('user')
    sum = count_c+count_u
    if sum is None:
        return jsonify('error: funcs not working'),400
    return jsonify(sum),200




