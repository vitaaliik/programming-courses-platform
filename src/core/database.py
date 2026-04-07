import sqlite3

from src.core.config import settings


def get_db_connection():
    conn = sqlite3.connect(settings.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn