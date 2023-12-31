import sqlite3

import sqlite3


class UserDB:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.create_user_table_if_not_exists()

    def create_user_table_if_not_exists(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                telegram_id TEXT,
                name TEXT
            )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def get_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user_data = self.cursor.fetchone()
        return user_data

    def get_by_telegram_id(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
        user_data = self.cursor.fetchone()
        return user_data

    def update(self, user_id, data):
        # data is a dictionary containing fields to update and their new values
        set_fields = ", ".join([f"{field}=? " for field in data.keys()])
        values = tuple(data.values()) + (user_id,)
        query = f"UPDATE users SET {set_fields}WHERE id=?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def create(self, data):
        # data is a dictionary containing user data
        fields = ", ".join(data.keys())
        values_placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())
        query = f"INSERT INTO users ({fields}) VALUES ({values_placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
