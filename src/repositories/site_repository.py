from src.core.database import get_db_connection


def get_site_content():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM site_content WHERE id = 1")
    content = cursor.fetchone()

    conn.close()

    return dict(content) if content else {}