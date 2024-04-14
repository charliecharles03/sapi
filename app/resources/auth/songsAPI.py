from ...models.model import create_songs_table, add_song, get_songs, update_song, delete_song, get_songId_from_name

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from flask import request, jsonify, session

def Add_song_route():
    if request.method == 'POST':
        add_song(request.form)
        return jsonify({"message": "Song added successfully!"}) 

@jwt_required()
def Get_songs_route():
    songs = get_songs()
    formatted_songs = [{'id': song[0], 'title': song[1], 'artist': song[2], 'album': song[3], 'duration': song[4], 'genre': song[5], 'year': song[6], 'cover': song[7], 'audio': song[8]} for song in songs]
    return jsonify(formatted_songs),200

def update_song_route():
    song_name= request.args.get('song_name')
    print(song_name)
    res = get_songId_from_name(song_name)
    print(res)
    if res is None:
        return jsonify('there is not song in this name')
    song_id = res[0][0]
    if request.method == 'POST':
        update_song(song_id, request.form)
    return jsonify('song successfully updated'),200

def delete_song_route():
    if request.method == 'DELETE':
        song_id = request.args.get('song_id');
        delete_song(song_id)
        return jsonify('song successfully deleted'),200


def get_song_by_id(song_name):
    if request.method == 'GET':
        name = get_songId_from_name(song_name)
        return jsonify(name),200
        
