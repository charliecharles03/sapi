import sqlite3
import hashlib

# Function to create database tables
def create_tables():
    print("Creating tables")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(100) NOT NULL,
            role VARCHAR(20) NOT NULL,
            email VARCHAR(50) NOT NULL
            )''')
    conn.commit()
    conn.close()

def create_songs_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                album TEXT,
                duration TEXT,
                genre TEXT,
                year INTEGER,
                cover TEXT,
                audio TEXT
                )''')
    conn.commit()
    conn.close()

def create_playlist_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS playlist (
                    id INTEGER PRIMARY KEY,
                    playlist_id INTEGER,
                    user_id INTEGER,
                    song_id INTEGER,
                    FOREIGN KEY(playlist_id) REFERENCES playlist_id(id)
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(song_id) REFERENCES songs(id)
                )''')
    conn.commit()
    conn.close()

def create_playlists_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS playlists (
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER,
                     name TEXT,
                     FOREIGN KEY(user_id) REFERENCES users(id)
             )''')
    conn.commit()
    conn.close()

def create_albums_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums (
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER,
                     name TEXT,
                     FOREIGN KEY(user_id) REFERENCES users(id)
             )''')
    conn.commit()
    conn.close()

def create_album_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS album(
                    id INTEGER PRIMARY KEY,
                    album_id INTEGER,
                    user_id INTEGER,
                    song_id INTEGER,
                    FOREIGN KEY(album_id) REFERENCES album_id(id)
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(song_id) REFERENCES songs(id)
                )''')
    conn.commit()
    conn.close()
#user part

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if username already exists
def check_username_exists(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user is not None

# Function to register a new user
def register_user(username, password, role,email):
    if check_username_exists(username):
        return 'Username already exists!'
    hashed_password = hash_password(password)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, role,email) VALUES (?, ?, ?,?)",
              (username, hashed_password, role,email))
    conn.commit()
    conn.close()
    return True

# Function to authenticate user login
def authenticate_user(username, password):
    create_tables()
    create_songs_table()
    hashed_password = hash_password(password)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

#songs part
def add_song(song_data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO songs (title, artist, album, duration, genre, year, cover, audio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (song_data['title'], song_data['artist'], song_data.get('album', ''), song_data.get('duration', ''), song_data.get('genre', ''), song_data.get('year', ''), song_data.get('cover', ''), song_data.get('audio', '')))
    conn.commit()
    conn.close()

def get_songs():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM songs")
    songs = c.fetchall()
    conn.close()
    return songs

def update_song(song_id, song_data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE songs SET title=?, artist=?, album=?, duration=?, genre=?, year=?, cover=?, audio=? WHERE id=?",
              (song_data['title'], song_data['artist'], song_data.get('album', ''), song_data.get('duration', ''), song_data.get('genre', ''), song_data.get('year', ''), song_data.get('cover', ''), song_data.get('audio', ''), song_id))
    conn.commit()
    conn.close()

def delete_song(song_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM songs WHERE id=?", (song_id,))
    conn.commit()
    conn.close()

def get_songId_from_name(song_name):
    print(song_name)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id FROM songs where title=?',(song_name,))
    song = c.fetchall()
    conn.close
    print(song)
    return song

#playlist part

def get_playlist(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print(user_id)
    try:
        cursor.execute('''SELECT playlists.name, songs.* FROM playlist
                        INNER JOIN songs ON playlist.song_id = songs.id
                        INNER JOIN playlists ON playlist.playlist_id = playlists.id
                        WHERE playlist.user_id = ?''', (user_id,))
        playlist = cursor.fetchall()
        print(playlist)
        conn.close()
        return playlist
    except sqlite3.Error as e:
        conn.close()
        raise e

def add_to_playlist(user_id, song_id, playlist_name):
    create_playlist_table()
    create_playlists_table()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        # Check if playlist exists for the user, if not, create it
        cursor.execute('''SELECT id FROM playlists
                        WHERE user_id = ? AND name = ?''', (user_id, playlist_name))
        playlist = cursor.fetchone()

        if not playlist:
            cursor.execute('''INSERT INTO playlists (user_id, name)
                            VALUES (?, ?)''', (user_id, playlist_name))
            playlist_id = cursor.lastrowid
        else:
            playlist_id = playlist[0]

        # Add song to playlist
        cursor.execute('''INSERT INTO playlist (playlist_id, user_id, song_id)
                        VALUES (?, ?, ?)''', (playlist_id, user_id, song_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise e


def delete_from_playlist(user_id, song_id, playlist_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        # Get playlist_id based on user_id and playlist_name
        cursor.execute('''SELECT id FROM playlists
                        WHERE user_id = ? AND name = ?''', (user_id, playlist_name))
        playlist = cursor.fetchone()

        if not playlist:
            return False  # Playlist not found

        playlist_id = playlist[0]

        # Delete song from playlist
        cursor.execute('''DELETE FROM playlist 
                        WHERE playlist_id = ? AND user_id = ? AND song_id = ?''', 
                       (playlist_id, user_id, song_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise e

#album part

def get_album(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print(user_id)
    try:
        cursor.execute('''SELECT albums.name, songs.* FROM album 
                        INNER JOIN songs ON album.song_id = songs.id
                        INNER JOIN albums ON album.album_id = albums.id
                        WHERE album.user_id = ?''', (user_id,))
        album = cursor.fetchall()
        conn.close()
        return album 
    except sqlite3.Error as e:
        conn.close()
        raise e

def add_to_album(user_id, song_id, album_name):
    create_album_table()
    create_albums_table()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        # Check if playlist exists for the user, if not, create it
        cursor.execute('''SELECT id FROM albums
                        WHERE user_id = ? AND name = ?''', (user_id, album_name))
        album = cursor.fetchone()

        if not album:
            cursor.execute('''INSERT INTO albums (user_id, name)
                            VALUES (?, ?)''', (user_id, album_name))
            album_id = cursor.lastrowid
        else:
            album_id = album[0]

        # Add song to playlist
        cursor.execute('''INSERT INTO album (album_id, user_id, song_id)
                        VALUES (?, ?, ?)''', (album_id, user_id, song_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        raise e

def update_album(album_name_old,album_name_new):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE album set album_name = ? where album_name = ?''',(album_name_new,album_name_old))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return false


def count_user(role):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT COUNT(*) FROM users where role = ? ''',(role,))
        count = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        return "not working"
    return count[0]

def count_album():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT COUNT(*) FROM albums''')
        count = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        return "not working"
    return count[0]

def count_songs():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT COUNT(*) FROM songs''')
        count = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        return "not working"
    return count[0]






