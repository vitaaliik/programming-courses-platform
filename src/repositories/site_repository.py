from src.core.database import get_db_connection


def get_site_content():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM site_content WHERE id = 1")
    content = cursor.fetchone()

    conn.close()

    return dict(content) if content else {}


def update_site_hero(hero_title: str, hero_subtitle: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE site_content
        SET hero_title = ?, hero_subtitle = ?
        WHERE id = 1
        """,
        (hero_title, hero_subtitle),
    )

    conn.commit()
    conn.close()


def get_home_blocks():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, content_html, sort_order
        FROM home_blocks
        ORDER BY sort_order ASC, id ASC
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


def create_home_block(title: str, content_html: str, sort_order: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO home_blocks (title, content_html, sort_order)
        VALUES (?, ?, ?)
        """,
        (title, content_html, sort_order),
    )

    conn.commit()
    conn.close()


def update_home_block(block_id: int, title: str, content_html: str, sort_order: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE home_blocks
        SET title = ?, content_html = ?, sort_order = ?
        WHERE id = ?
        """,
        (title, content_html, sort_order, block_id),
    )

    conn.commit()
    conn.close()


def delete_home_block(block_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM home_blocks WHERE id = ?", (block_id,))

    conn.commit()
    conn.close()