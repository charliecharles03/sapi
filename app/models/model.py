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
