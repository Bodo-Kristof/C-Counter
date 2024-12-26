from flask import Flask, jsonify, request
import sqlite3
import os
from flask_cors import CORS  # Importáljuk a CORS-t

app = Flask(__name__)

# Engedélyezzük a CORS-t minden kéréshez
CORS(app)

# Az alkalmazás mappájában tároljuk az adatbázist
DATABASE = os.path.join(os.path.dirname(__file__), 'counter.db')

# Adatbázis inicializálás
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            value INTEGER NOT NULL
        )
        """)
        cursor.execute("INSERT OR IGNORE INTO counter (id, value) VALUES (1, 0)")
        conn.commit()

@app.route('/get_counter', methods=['GET'])
def get_counter():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM counter WHERE id = 1")
        value = cursor.fetchone()[0]
        return jsonify({'value': value})

@app.route('/increment', methods=['POST'])
def increment_counter():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE counter SET value = value + 1 WHERE id = 1")
        conn.commit()
        cursor.execute("SELECT value FROM counter WHERE id = 1")
        value = cursor.fetchone()[0]
        return jsonify({'value': value})

@app.route('/reset', methods=['POST'])
def reset_counter():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE counter SET value = 0 WHERE id = 1")
        conn.commit()
        cursor.execute("SELECT value FROM counter WHERE id = 1")
        value = cursor.fetchone()[0]
        return jsonify({'value': value})

@app.route('/decrement', methods=['POST'])
def decrement_counter():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE counter SET value = value - 1 WHERE id = 1")
        conn.commit()
        cursor.execute("SELECT value FROM counter WHERE id = 1")
        value = cursor.fetchone()[0]
        return jsonify({'value': value})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)  # Flask szerver 5000-es porton
