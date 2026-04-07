from src.core.database import get_db_connection


def get_profile_data(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, email, created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return None

    user = dict(user)

    cursor.execute(
        """
        SELECT test_results.score, test_results.total, test_results.passed_at, courses.title, courses.slug
        FROM test_results
        JOIN courses ON test_results.course_id = courses.id
        WHERE test_results.user_id = ?
        ORDER BY test_results.passed_at DESC
        """,
        (user_id,),
    )
    results = cursor.fetchall()
    results = [dict(r) for r in results]

    total_tests = len(results)

    if total_tests > 0:
        avg_score = sum((r["score"] / r["total"]) * 100 for r in results) / total_tests
        best_score = max((r["score"] / r["total"]) * 100 for r in results)
    else:
        avg_score = 0
        best_score = 0

    cursor.execute("SELECT COUNT(*) as total FROM courses")
    total_courses = cursor.fetchone()["total"]

    completed_courses = len(set(r["title"] for r in results))
    progress_percent = round((completed_courses / total_courses) * 100, 1) if total_courses > 0 else 0

    recent_results = results[:4]

    conn.close()

    return {
        "profile_user": user,
        "results": results,
        "recent_results": recent_results,
        "total_tests": total_tests,
        "avg_score": round(avg_score, 1),
        "best_score": round(best_score, 1),
        "completed_courses": completed_courses,
        "total_courses": total_courses,
        "progress_percent": progress_percent,
    }