from services.users import UserDB
from services.group import GroupDB
from services.requests import RequestDB
import sqlite3


conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()
User = UserDB(conn, cursor)
Group = GroupDB(conn, cursor)
Request = RequestDB(conn, cursor)