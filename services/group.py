import sqlite3


class GroupDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_by_id(self, group_id):
        self.cursor.execute("SELECT * FROM groups WHERE id=?", (group_id,))
        group_data = self.cursor.fetchone()
        return group_data

    def get_by_elder_id(self, elder_id):
        self.cursor.execute("SELECT * FROM groups WHERE elder_id=?", (elder_id,))
        group_data = self.cursor.fetchone()
        return group_data

    def create(self, group_id, elder_id, data):
        # data is a dictionary containing group data
        fields = "id, elder_id, " + ", ".join(data.keys())
        values_placeholders = "?, ?" + (", ?" * len(data))
        values = (group_id, elder_id) + tuple(data.values())
        query = f"INSERT INTO groups ({fields}) VALUES ({values_placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def update(self, group_id, data):
        # data is a dictionary containing fields to update and their new values
        set_fields = ", ".join([f"{field}=? " for field in data.keys()])
        values = tuple(data.values()) + (group_id,)
        query = f"UPDATE groups SET {set_fields}WHERE id=?"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, group_id):
        self.cursor.execute("DELETE FROM groups WHERE id=?", (group_id,))
        self.conn.commit()

    def get_by_name(self, group_name):
        self.cursor.execute("SELECT * FROM groups WHERE name=?", (group_name,))
        group_data = self.cursor.fetchone()
        return group_data

    def add_to_group(self, group_id, user_id):
        self.cursor.execute("INSERT INTO group_membership (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
        self.conn.commit()

    def remove_from_group(self, group_id, user_id):
        self.cursor.execute("DELETE FROM group_membership WHERE user_id=? AND group_id=?", (user_id, group_id))
        self.conn.commit()

    def get_all_users_by_group(self, group_id):
        self.cursor.execute(
            "SELECT * FROM users JOIN group_membership ON users.id = group_membership.user_id WHERE group_membership.group_id=?",
            (group_id,))
        users_data = self.cursor.fetchall()
        return users_data