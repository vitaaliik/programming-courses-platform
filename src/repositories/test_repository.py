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


def get_test_questions_by_course_id(course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            allow_multiple,
            is_a_correct,
            is_b_correct,
            is_c_correct,
            is_d_correct,
            sort_order
        FROM test_questions
        WHERE course_id = ?
        ORDER BY sort_order ASC, id ASC
        """,
        (course_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def create_test_question(
    course_id: int,
    question: str,
    option_a: str,
    option_b: str,
    option_c: str,
    option_d: str,
    allow_multiple: int,
    is_a_correct: int,
    is_b_correct: int,
    is_c_correct: int,
    is_d_correct: int,
    sort_order: int,
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO test_questions (
            course_id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            allow_multiple,
            is_a_correct,
            is_b_correct,
            is_c_correct,
            is_d_correct,
            sort_order
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            course_id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            allow_multiple,
            is_a_correct,
            is_b_correct,
            is_c_correct,
            is_d_correct,
            sort_order,
        ),
    )

    conn.commit()
    conn.close()


def update_test_question(
    question_id: int,
    question: str,
    option_a: str,
    option_b: str,
    option_c: str,
    option_d: str,
    allow_multiple: int,
    is_a_correct: int,
    is_b_correct: int,
    is_c_correct: int,
    is_d_correct: int,
    sort_order: int,
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE test_questions
        SET
            question = ?,
            option_a = ?,
            option_b = ?,
            option_c = ?,
            option_d = ?,
            allow_multiple = ?,
            is_a_correct = ?,
            is_b_correct = ?,
            is_c_correct = ?,
            is_d_correct = ?,
            sort_order = ?
        WHERE id = ?
        """,
        (
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            allow_multiple,
            is_a_correct,
            is_b_correct,
            is_c_correct,
            is_d_correct,
            sort_order,
            question_id,
        ),
    )

    conn.commit()
    conn.close()


def delete_test_question(question_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM test_questions WHERE id = ?",
        (question_id,),
    )

    conn.commit()
    conn.close()