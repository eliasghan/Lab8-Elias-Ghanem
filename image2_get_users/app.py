import os
import sqlite3

from flask import Flask, jsonify
from flask_cors import CORS

DB_PATH = os.environ.get(
    "DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
)
PORT = 3000

DEFAULT_USERS = [
    {
        "name": "John Doe",
        "email": "jondoe@gamil.com",
        "phone": "067765434567",
        "address": "John Doe Street, Innsbruck",
        "country": "Austria",
    },
    {
        "name": "Jane Smith",
        "email": "janesmith@gmail.com",
        "phone": "03123456",
        "address": "Hamra Street, Beirut",
        "country": "Lebanon",
    },
    {
        "name": "Mary James",
        "email": "maryjames@gmail.com",
        "phone": "09878766676",
        "address": "Broadway Street, New York",
        "country": "United States",
    },
]


def connect_to_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the users table and insert the default users on the first run."""
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO users (name, email, phone, address, country) "
                "VALUES (:name, :email, :phone, :address, :country)",
                DEFAULT_USERS,
            )
        conn.commit()
    finally:
        conn.close()


def get_user_names():
    """Return the names of all the users in the database."""
    names = []
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users ORDER BY user_id")
        names = [row[0] for row in cur.fetchall()]
    except sqlite3.Error:
        names = []
    finally:
        if conn is not None:
            conn.close()
    return names


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/get_users", methods=["GET"])
@app.route("/api/get_users", methods=["GET"])
def api_get_users():
    return jsonify(get_user_names())


if __name__ == "__main__":
    init_db()
    # 0.0.0.0 makes the API reachable from outside the container (docker run -p 3000:3000)
    app.run(host="0.0.0.0", port=PORT)
