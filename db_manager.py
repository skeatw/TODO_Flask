import sqlite3
from datetime import datetime

class Manage:

    @classmethod
    def create_connection(cls):
        conn = sqlite3.connect('tasks.db')
        cur = conn.cursor()

        # TODO: сначала набросать как будет выглядеть бд, а потом уже создавать все таблицы
        cur.execute('')
        conn.commit()
        conn.close()

    def add_to_db(self, data: list[None | str | datetime | bool]) -> None:
        pass
