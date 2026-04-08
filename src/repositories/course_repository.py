from src.core.database import get_db_connection


def get_course_by_slug(slug: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, slug, title, description, content_file, page_title, page_subtitle
        FROM courses
        WHERE slug = ?
        """,
        (slug,),
    )
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def create_course(slug: str, title: str, description: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO courses (slug, title, description, content_file, page_title, page_subtitle)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            slug,
            title,
            description,
            f"{slug}.html",
            f"Курс: {title}",
            description,
        ),
    )

    conn.commit()
    conn.close()