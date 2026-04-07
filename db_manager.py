import sqlite3
from datetime import datetime

class Manage:

    @classmethod
    def create_connection(cls):
        conn = sqlite3.connect('todo.db')
        cur = conn.cursor()

        # TODO: сначала набросать как будет выглядеть бд, а потом уже создавать все таблицы
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) UNIQUE)''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(250),
            creation_time TIMESTAMP,
            completed_time TIMESTAMP,
            lead_time TIMESTAMP,
            status BOOL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE)
        ''')
        conn.commit()
        conn.close()

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def __del__(self):
        self.conn.close()

    def add_to_db(self, data: list[None | str | datetime | bool]) -> None:
        pass
