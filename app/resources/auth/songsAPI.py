from ...models.model import create_songs_table, add_song, get_songs, update_song, delete_song

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from flask import request, jsonify, session

@jwt_required()
def Add_song_route():
    if request.method == 'POST':
        add_song(request.form)
        return jsonify({"message": "Song added successfully!"}) 

@jwt_required()
def Get_songs_route():
    songs = get_songs()
    formatted_songs = [{'id': song[0], 'title': song[1], 'artist': song[2], 'album': song[3], 'duration': song[4], 'genre': song[5], 'year': song[6], 'cover': song[7], 'audio': song[8]} for song in songs]
    return jsonify(formatted_songs),200

@jwt_required()
def update_song_route(song_id):
    if request.method == 'POST':
        update_song(song_id, request.form)
        return redirect(url_for('get_songs'))

@jwt_required()
def delete_song_route(song_id):
    if request.method == 'POST':
        delete_song(song_id)
        return redirect(url_for('get_songs'))
