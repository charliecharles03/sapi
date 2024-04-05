from ...models.model import create_songs_table, add_song, get_songs, update_song, delete_song

from flask import request, jsonify, session

def Add_song_route():
    if request.method == 'POST':
        add_song(request.form)
        return jsonify({"message": "Song added successfully!"}) 

def Get_songs_route():
    songs = get_songs()
    return render_template('songs.html', songs=songs)

def update_song_route(song_id):
    if request.method == 'POST':
        update_song(song_id, request.form)
        return redirect(url_for('get_songs'))

def delete_song_route(song_id):
    if request.method == 'POST':
        delete_song(song_id)
        return redirect(url_for('get_songs'))
