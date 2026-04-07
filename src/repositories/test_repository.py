from src.core.database import get_db_connection


def save_test_result(user_id: int, course_id: int, score: int, total: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO test_results (user_id, course_id, score, total)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, course_id, score, total),
    )

    conn.commit()
    conn.close()