import sqlite3
from datetime import datetime

class Manage:

    def __init__(self):
        self.db_path = 'todo.db'
        self._create_connection()

    def _create_connection(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # TODO: сначала набросать как будет выглядеть бд, а потом уже создавать все таблицы
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            token VARCHAR(32) UNIQUE,
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

    def add_to_db_task(self, data: list[None | str | datetime | bool]) -> None:
        """
        Добавление в таблицу task информацию о созданной задачи
        :param data: список, в котором находится информация о созданной задачи
        :return: None
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        title = data[0]
        desc = data[1]
        creation_time = data[2]
        status = data[3]
        cur.execute('INSERT OR IGNORE INTO tasks (title, description, creation_time, status) VALUES (?, ?, ?, ?)', (title, desc, creation_time, status))
        conn.commit()
        conn.close()

    def add_to_db_user(self, data: list[str]) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        username = data[0]
        email = data[1]

        cur.execute('INSERT OR IGNORE INTO user (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
        conn.close()

    def get_email(self, username: str) -> str:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        user_email = cur.execute('SELECT email FROM user WHERE username = ?', (username, )).fetchone()[0]

        conn.close()
        return user_email

    def get_id_by_token(self, token: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        id_str = cur.execute('SELECT id FROM user WHERE token = ?', (token, )).fetchone()[0]
        id_user = int(id_str)
        conn.close()

        return id_user

    def add_token_to_db(self, token: str, username: str) -> None:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()


        cur.execute('UPDATE user SET token = ? WHERE username = ? ', (token, username))

        conn.commit()
        conn.close()

    def is_there_a_user_in_db(self, username: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        answer = cur.execute('SELECT id FROM user WHERE username = ?', (username, )).fetchone()
        if answer is not None:
            return True
        return False


manage = Manage()
