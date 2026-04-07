from src.core.database import get_db_connection


def get_course_with_sections_by_slug(slug: str):
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
    course = cursor.fetchone()

    if not course:
        conn.close()
        return None

    course_dict = dict(course)

    cursor.execute(
        """
        SELECT id, course_id, title, content_html, sort_order, created_at
        FROM course_sections
        WHERE course_id = ?
        ORDER BY sort_order ASC, id ASC
        """,
        (course_dict["id"],),
    )
    sections = cursor.fetchall()

    conn.close()

    course_dict["sections"] = [dict(section) for section in sections]
    return course_dict


def get_all_courses_for_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, slug, title, description, page_title, page_subtitle
        FROM courses
        ORDER BY title ASC
        """
    )
    courses = cursor.fetchall()

    conn.close()
    return [dict(course) for course in courses]


def update_course_main_info(course_id: int, page_title: str, page_subtitle: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET page_title = ?, page_subtitle = ?
        WHERE id = ?
        """,
        (page_title, page_subtitle, course_id),
    )

    conn.commit()
    conn.close()


def create_course_section(course_id: int, title: str, content_html: str, sort_order: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO course_sections (course_id, title, content_html, sort_order)
        VALUES (?, ?, ?, ?)
        """,
        (course_id, title, content_html, sort_order),
    )

    conn.commit()
    conn.close()


def update_course_section(section_id: int, title: str, content_html: str, sort_order: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE course_sections
        SET title = ?, content_html = ?, sort_order = ?
        WHERE id = ?
        """,
        (title, content_html, sort_order, section_id),
    )

    conn.commit()
    conn.close()


def delete_course_section(section_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM course_sections
        WHERE id = ?
        """,
        (section_id,),
    )

    conn.commit()
    conn.close()