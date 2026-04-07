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

    def add_to_db_task(self, data: list[None | str | datetime | bool]) -> None:
        """
        Добавление в таблицу task информацию о созданной задачи
        :param data: список, в котором находится информация о созданной задачи
        :return: None
        """
        cur = self.conn.cursor()
        title = data[0]
        desc = data[1]
        creation_time = data[2]
        status = data[3]
        cur.execute('INSERT OR IGNORE INTO tasks (title, description, creation_time, status) VALUES (?, ?, ?, ?)', (title, desc, creation_time, status))
        self.conn.commit()
        cur.close()

    def add_to_db_user(self, data: list[str]) -> None:
        cur = self.conn.cursor()
        username = data[0]
        email = data[1]

        cur.execute('INSERT OR IGNORE INTO user (username, email) VALUES (?, ?)', (username, email))
        self.conn.commit()
        cur.close()

