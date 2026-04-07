from src.core.database import get_db_connection
from src.repositories.site_repository import get_site_content


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

    site_content = get_site_content()

    conn.close()

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_results": total_results,
        "users": users,
        "recent_results": recent_results,
        "site_content": site_content,
    }


def update_home_page_content(data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE site_content
        SET
            hero_title = ?,
            hero_subtitle = ?,

            about_title = ?,
            about_text_1 = ?,
            about_text_2 = ?,

            audience_title = ?,
            audience_item_1 = ?,
            audience_item_2 = ?,
            audience_item_3 = ?,
            audience_item_4 = ?,

            features_title = ?,
            features_item_1 = ?,
            features_item_2 = ?,
            features_item_3 = ?,
            features_item_4 = ?,
            features_item_5 = ?,

            college_title = ?,
            college_text_1 = ?,
            college_text_2 = ?,

            creator_title = ?,
            creator_text = ?,

            skills_title = ?,
            skills_text_1 = ?,
            skills_text_2 = ?,

            importance_title = ?,
            importance_text_1 = ?,
            importance_text_2 = ?
        WHERE id = 1
        """,
        (
            data["hero_title"],
            data["hero_subtitle"],
            data["about_title"],
            data["about_text_1"],
            data["about_text_2"],
            data["audience_title"],
            data["audience_item_1"],
            data["audience_item_2"],
            data["audience_item_3"],
            data["audience_item_4"],
            data["features_title"],
            data["features_item_1"],
            data["features_item_2"],
            data["features_item_3"],
            data["features_item_4"],
            data["features_item_5"],
            data["college_title"],
            data["college_text_1"],
            data["college_text_2"],
            data["creator_title"],
            data["creator_text"],
            data["skills_title"],
            data["skills_text_1"],
            data["skills_text_2"],
            data["importance_title"],
            data["importance_text_1"],
            data["importance_text_2"],
        ),
    )

    conn.commit()
    conn.close()


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