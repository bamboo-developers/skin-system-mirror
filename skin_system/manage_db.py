import sqlite3
from typing import Literal
import skin_system
from .get_path import *
from flask import jsonify
import os
import requests

USER_DATA = 'user_data'
SKIN_DATA = 'skin_data'


def connect_to_db():
    project_root = get_path('skin-system.db', '..')  # noqa: F405
    return sqlite3.connect(project_root)

def create_db():
    with connect_to_db() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id TEXT UNIQUE,
                nickname TEXT,
                redirect_from_ely INTEGER DEFAULT 1,
                redirect_nickname TEXT,
                skin_id TEXT
            )
        """)
        connection.commit()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS skin_data (
                        id TEXT UNIQUE,
                        skin TEXT,
                        value TEXT,
                        signature TEXT
                    )
                """)
        connection.commit()

class ManageDB():
    def __init__(self):
        pass

    def create_user(self, nickname, redirect_ely=1, need_exist=True):
        with connect_to_db() as connection:
            if need_exist:
                if self.record_exists(USER_DATA, 'nickname', nickname):
                    return None
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO user_data (id, nickname, redirect_from_ely) VALUES (?, ?, ?)''',
                           (skin_system.generate_id(), nickname, redirect_ely))
            connection.commit()

            return '''SELECT id FROM user_data WHERE nickname = ? LIMIT 1''', (nickname,)


    def record_exists(self, table_name, column_name, value):
        query = f'''SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1'''
        with connect_to_db() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (value,))
            return cursor.fetchone() is not None

    def redirect_state(self, nickname):
        with connect_to_db() as connection:
            cursor = connection.cursor()
            if not self.record_exists(USER_DATA, 'nickname', nickname):
                return 1

            cursor.execute('''SELECT redirect_from_ely FROM user_data WHERE nickname = ? LIMIT 1''', (nickname,))
            need_redirect = cursor.fetchone()

            return need_redirect[0]


    def get_sign_skin(self, skin_image):
        base64_skin = skin_system.encode(skin_image)

        with connect_to_db() as connection:
            cursor = connection.cursor()

            if self.record_exists(SKIN_DATA, 'skin', base64_skin):
                cursor.execute('''SELECT id FROM skin_data WHERE skin = ? LIMIT 1''', (base64_skin,))
                result = cursor.fetchone()
                return result[0]

            result = skin_system.sign_skin(skin_image)
            if 'value' not in result or 'signature' not in result:
                return {"message": result, "code": 500}

            skin_id = skin_system.generate_id(12)

            cursor.execute('''INSERT INTO skin_data (id, skin, value, signature) VALUES (?, ?, ?, ?)''',
                           (skin_id, base64_skin, result['value'], result['signature']))
            connection.commit()
            return skin_id

    def nickname_exists_ely(self, nickname=None, redirect_nickname=None):
        with connect_to_db() as connection:
            cursor = connection.cursor()

            if nickname is not None and redirect_nickname is not None:
                cursor.execute('''SELECT * FROM user_data WHERE nickname = ? OR redirect_from_ely = ?
                                  OR nickname = ? OR redirect_from_ely = ?;''',
                               (nickname, nickname, redirect_nickname, redirect_nickname))
            elif nickname is not None:
                cursor.execute('''SELECT * FROM user_data WHERE nickname = ? OR redirect_from_ely = ?;''',
                               (nickname, nickname))
            elif redirect_nickname is not None:
                cursor.execute('''SELECT * FROM user_data WHERE nickname = ? OR redirect_from_ely = ?;''',
                               (redirect_nickname, redirect_nickname))
            else:
                return jsonify({"message": "nickname and redirected nickname are empty", "code": 400}), 400

            return cursor.fetchone()

    def set_redirected_nickname_ely(self, nickname, redirect_nickname):
        if not self.nickname_exists_ely(nickname, redirect_nickname):
            self.create_user(nickname)

        if self.record_exists(USER_DATA, 'redirect_nickname', redirect_nickname):
            return False

        with connect_to_db() as connection:
            cursor = connection.cursor()
            if redirect_nickname == '<del>':
                redirect_nickname = None

            cursor.execute('''UPDATE user_data SET redirect_nickname = ? WHERE nickname = ?''',
                           (redirect_nickname, nickname))
            connection.commit()

        return True

    def toggle_redirect(self, nickname, toggle: Literal[0, 1]):
        with connect_to_db() as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE user_data SET redirect_from_ely = ? WHERE nickname = ?''',
                           (toggle, nickname))
            connection.commit()

        return True

    def view_on_db(self, table_name: Literal["user_data", "skin_data"], nickname=None, user_id=None, skin_id=None):
        with connect_to_db() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            if nickname == "<all>":
                cursor.execute(f'''SELECT * FROM {table_name}''')
                result = cursor.fetchall()
            else:
                if skin_id:
                    cursor.execute('''SELECT * FROM skin_data WHERE id = ?''', (skin_id,))
                    result = cursor.fetchall()
                    return [dict(row) for row in result]

                cursor.execute('''SELECT * FROM user_data WHERE nickname = ? OR id = ?''', (nickname, user_id))
                result = cursor.fetchall()

            return [dict(row) for row in result]

    def what_redirect_of(self, nickname, return_system: Literal['skin_system', 'ely'] = 'auto'):
        with connect_to_db() as connection:
            cursor = connection.cursor()
            state = self.redirect_state(nickname)

            if state == 1:
                cursor.execute("""SELECT redirect_nickname FROM user_data WHERE nickname = ?""", (nickname,))
                result = cursor.fetchone()
                if result is None or result[0] is None:
                    return {'ely': nickname}

                return {'ely': result[0]}
            else:
                if return_system == 'auto':
                    return {'skin_system': nickname}

                return {f'{return_system}': nickname}

    def set_skin_id(self,nickname, skin_id):
        if not self.record_exists(USER_DATA, 'nickname', nickname):
            self.create_user(nickname)

        with connect_to_db() as connection:
            cursor = connection.cursor()


            cursor.execute('''UPDATE user_data SET skin_id = ? WHERE nickname = ?''',
                           (skin_id, nickname))
            connection.commit()

        return True

    def remove_row(self, table_name: Literal["user_data", "skin_data"], skin_id=None, user_id=None, nickname=None):
        conditions = []
        values = []

        if skin_id is not None:
            conditions.append('id = ?')
            values.append(skin_id)
        if user_id is not None:
            conditions.append('id = ?')
            values.append(user_id)
        if nickname is not None:
            conditions.append('nickname = ?')
            values.append(nickname)

        if not conditions:
            return False

        query = f'''DELETE FROM {table_name} WHERE {' OR '.join(conditions)}'''

        with connect_to_db() as connection:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()

        return True

    def proxy_from_ely(self, **kwargs):
        if 'url' not in kwargs:
            raise ValueError("You must provide 'url'")

        url = kwargs['url']
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"message": f"Can't load skin data, {response.status_code}: {response.text}", "code": 500}

    def return_texture_data_for_system(self, **kwargs):
        skin_data =None

        if 'nickname' not in kwargs and 'user_id' not in kwargs:
            raise ValueError("You must provide either 'nickname' or 'user_id'")

        if 'proxy' not in kwargs:
            proxy = False
        else:
            proxy = kwargs['proxy']

        if 'nickname' in kwargs and 'user_id' in kwargs:
            raise ValueError("You can provide either 'nickname' or 'user_id', not both")

        if 'nickname' in kwargs:
            value = 'nickname'
        else:
            value = 'id'

        with connect_to_db() as connection:
            cursor = connection.cursor()

            user_data = f'''SELECT id, nickname, skin_id FROM user_data WHERE {value} = ?'''
            cursor.execute(user_data, (kwargs[value],))
            user_data = cursor.fetchall()[0]

            if  user_data[2]:
                skin_data = '''SELECT value, signature FROM skin_data WHERE id = ?'''
                cursor.execute(skin_data, (user_data[2],))
                skin_data = cursor.fetchall()[0]
            else:
                if proxy:
                    return self.proxy_from_ely(url=f'http://skinsystem.ely.by/textures/signed/{user_data[1]}?proxy=true')
                else:
                    skin_data = ["None record on database", ""]

            data = {
                "id": user_data[0],
                "name": user_data[1],
                "properties": [
                    {
                        "name": "textures",
                        "signature": skin_data[1],
                        "value": skin_data[0]
                    },
                    {
                        "name": str(os.environ.get("SKIN_SYSTEM_NAME")),
                        "value": "I know why you are asking)"
                    }
                ]
            }

        return data