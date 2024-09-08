import sqlite3
from .get_path import *
from flask import jsonify


def connect_to_db():
    project_root = get_path('skin-system.db', '..')
    return sqlite3.connect(project_root)


def create_db():
    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS redirected_nicknames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT,
                redirect TEXT
            )
        """)
        connection.commit()


def nickname_exists(nickname=None, redirect_nickname=None):
    with connect_to_db() as connection:
        cursor = connection.cursor()

        if nickname is not None and redirect_nickname is not None:
            cursor.execute('''SELECT * FROM redirected_nicknames
                              WHERE nickname = ? OR redirect = ?
                              OR nickname = ? OR redirect = ?;''',
                           (nickname, nickname, redirect_nickname, redirect_nickname))
        elif nickname is not None:
            cursor.execute('''SELECT * FROM redirected_nicknames
                              WHERE nickname = ? OR redirect = ?;''',
                           (nickname, nickname))
        elif redirect_nickname is not None:
            cursor.execute('''SELECT * FROM redirected_nicknames
                              WHERE nickname = ? OR redirect = ?;''',
                           (redirect_nickname, redirect_nickname))
        else:
            return jsonify({"message": "nickname and redirected nickname are empty", "code": 400}), 400

        return cursor.fetchone() is not None

def what_redirect_of(username):
    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT redirect FROM redirected_nicknames WHERE nickname = ?""", (username,))

        result = cursor.fetchone()
        if result is None:
            return username

        return result[0]


def add_nickname(nickname, redirect_nickname):
    if nickname_exists(nickname, redirect_nickname):
        return jsonify({"message": "nickname or redirected nickname already exists", "code": 409}), 409

    data = nickname, redirect_nickname
    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO redirected_nicknames (nickname, redirect) 
            VALUES (?, ?)
        """, data)
        connection.commit()

    return jsonify({"message": "data added successfully", "code": 200}), 200


def remove_nickname(nickname):
    if not nickname_exists(nickname):
        return {"message": "no nickname to delete", "code": 404}, 404

    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute(""" DELETE FROM redirected_nicknames WHERE nickname = ?""", (nickname,))
        connection.commit()

    return {"message": "data deleted successfully", "code": 200}, 200


def search_on_db(nickname):
    with connect_to_db() as connection:
        cursor = connection.cursor()
        if nickname != "<all>":
            cursor.execute('''SELECT nickname, redirect FROM redirected_nicknames WHERE nickname = ?''', (nickname,))
        else:
            cursor.execute("SELECT nickname, redirect FROM redirected_nicknames")

        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]

        if not data:
            return jsonify({"message": "no nickname found", "code": 404}), 404

        return jsonify(data), 200
