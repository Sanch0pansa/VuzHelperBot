import sqlite3
import time


class RequestDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_by_id(self, request_id):
        self.cursor.execute("SELECT * FROM requests WHERE id=?", (request_id,))
        request_data = self.cursor.fetchone()
        return request_data

    def create(self, group_id, data):
        # data is a dictionary containing request data
        fields = "group_id, " + ", ".join(data.keys())
        values_placeholders = "?, " + (", ?" * len(data))
        values = (group_id,) + tuple(data.values())
        query = f"INSERT INTO requests ({fields}) VALUES ({values_placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def update(self, request_id, data):
        # data is a dictionary containing fields to update and their new values
        set_fields = ", ".join([f"{field}=? " for field in data.keys()])
        values = tuple(data.values()) + (request_id,)
        query = f"UPDATE requests SET {set_fields}WHERE id=?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, request_id):
        self.cursor.execute("DELETE FROM requests WHERE id=?", (request_id,))
        self.conn.commit()

    def get_all_requests_by_group(self, group_id):
        self.cursor.execute("SELECT * FROM requests WHERE group_id=?", (group_id,))
        requests_data = self.cursor.fetchall()
        return requests_data

    def answer_request(self, user_id, request_id, status):
        # status is a string representing the request status
        created_at = time.strftime('%Y-%m-%d %H:%M:%S')
        values = (request_id, user_id, status, created_at)
        query = "INSERT INTO request_answers (request_id, user_id, request_status, created_at) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_request_answers(self, request_id):
        query = """
            SELECT ra.id, ra.request_id, ra.request_status, ra.created_at, ra.updated_at, 
                   u.username, u.telegram_id, u.name 
            FROM request_answers ra 
            JOIN users u ON ra.user_id = u.id 
            WHERE ra.request_id=?
        """
        self.cursor.execute(query, (request_id,))
        answers_data = self.cursor.fetchall()
        return answers_data
