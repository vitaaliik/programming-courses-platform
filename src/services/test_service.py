from src.data.tests_data import TESTS
from src.repositories.course_repository import get_course_by_slug
from src.repositories.test_repository import save_test_result


def get_test_by_course_name(course_name: str):
    return TESTS.get(course_name)


def calculate_test_result(form, questions):
    score = 0
    total = len(questions)
    detailed_results = []

    for q in questions:
        user_answer = form.get(q["id"])
        is_correct = user_answer == q["correct"]

        if is_correct:
            score += 1

        detailed_results.append(
            {
                "question": q["question"],
                "user_answer": user_answer if user_answer else "Не вибрано",
                "correct_answer": q["correct"],
                "is_correct": is_correct,
            }
        )

    return score, total, detailed_results


def save_result_if_logged_in(user_id: int | None, course_name: str, score: int, total: int):
    if not user_id:
        return

    course_row = get_course_by_slug(course_name)
    if not course_row:
        return

    course_id = course_row["id"]
    save_test_result(user_id, course_id, score, total)