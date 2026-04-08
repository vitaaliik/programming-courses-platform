from src.core.database import get_db_connection
from src.repositories.site_repository import (
    create_home_block,
    delete_home_block,
    get_home_blocks,
    get_site_content,
    update_home_block,
    update_site_hero,
)


def get_admin_dashboard_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) as total_courses FROM courses")
    total_courses = cursor.fetchone()["total_courses"]

    cursor.execute("SELECT COUNT(*) as total_results FROM test_results")
    total_results = cursor.fetchone()["total_results"]

    cursor.execute(
        """
        SELECT
            u.id,
            u.username,
            u.email,
            u.role,
            u.created_at,
            COUNT(tr.id) as tests_passed,
            COALESCE(ROUND(AVG((tr.score * 100.0) / tr.total), 1), 0) as avg_result,
            COUNT(DISTINCT tr.course_id) as completed_courses,
            MAX(tr.passed_at) as last_activity
        FROM users u
        LEFT JOIN test_results tr ON u.id = tr.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
        """
    )
    users = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            u.username,
            u.email,
            c.title as course_title,
            tr.score,
            tr.total,
            tr.passed_at
        FROM test_results tr
        JOIN users u ON tr.user_id = u.id
        JOIN courses c ON tr.course_id = c.id
        ORDER BY tr.passed_at DESC
        LIMIT 12
        """
    )
    recent_results = cursor.fetchall()

    conn.close()

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_results": total_results,
        "users": users,
        "recent_results": recent_results,
    }


def update_home_hero(data: dict):
    update_site_hero(
        hero_title=data["hero_title"].strip(),
        hero_subtitle=data["hero_subtitle"].strip(),
    )


def get_home_editor_data():
    return {
        "site_content": get_site_content(),
        "home_blocks": get_home_blocks(),
    }


def add_new_home_block(title: str, content_html: str, sort_order: int):
    if not title.strip():
        return False

    create_home_block(title.strip(), content_html.strip(), sort_order)
    return True


def save_home_block(block_id: int, title: str, content_html: str, sort_order: int):
    if not title.strip():
        return False

    update_home_block(block_id, title.strip(), content_html.strip(), sort_order)
    return True


def remove_home_block(block_id: int):
    delete_home_block(block_id)
    return True


def make_user_admin_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET role = 'admin'
        WHERE email = ?
        """,
        (email,),
    )

    conn.commit()
    conn.close()