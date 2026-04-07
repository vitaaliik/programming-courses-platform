from src.core.database import get_db_connection


def get_course_by_slug(slug: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, slug FROM courses WHERE slug = ?", (slug,))
    course = cursor.fetchone()

    conn.close()
    return course