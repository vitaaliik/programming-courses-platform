from src.repositories.course_repository import get_course_by_slug
from src.repositories.test_repository import (
    create_test_question,
    delete_test_question,
    get_test_questions_by_course_id,
    save_test_result,
    update_test_question,
)


def _extract_correct_options(row: dict):
    correct_options = []

    if row["is_a_correct"]:
        correct_options.append(row["option_a"])
    if row["is_b_correct"]:
        correct_options.append(row["option_b"])
    if row["is_c_correct"]:
        correct_options.append(row["option_c"])
    if row["is_d_correct"]:
        correct_options.append(row["option_d"])

    return correct_options


def get_test_by_course_name(course_name: str):
    course_row = get_course_by_slug(course_name)
    if not course_row:
        return None

    questions_rows = get_test_questions_by_course_id(course_row["id"])

    questions = []
    for row in questions_rows:
        questions.append(
            {
                "id": f"q{row['id']}",
                "db_id": row["id"],
                "question": row["question"],
                "options": [
                    row["option_a"],
                    row["option_b"],
                    row["option_c"],
                    row["option_d"],
                ],
                "allow_multiple": bool(row["allow_multiple"]),
                "correct_options": _extract_correct_options(row),
                "sort_order": row["sort_order"],
                "is_a_correct": row["is_a_correct"],
                "is_b_correct": row["is_b_correct"],
                "is_c_correct": row["is_c_correct"],
                "is_d_correct": row["is_d_correct"],
            }
        )

    return {
        "title": f"Тест: {course_row['title']}",
        "course_id": course_row["id"],
        "questions": questions,
    }


def calculate_test_result(form, questions):
    score = 0
    total = len(questions)
    detailed_results = []

    for q in questions:
        field_name = q["id"]
        user_answers = form.getlist(field_name)
        correct_answers = q["correct_options"]

        is_correct = set(user_answers) == set(correct_answers)

        if is_correct:
            score += 1

        detailed_results.append(
            {
                "question": q["question"],
                "user_answer": ", ".join(user_answers) if user_answers else "Не вибрано",
                "correct_answer": ", ".join(correct_answers),
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

    save_test_result(user_id, course_row["id"], score, total)


def get_test_editor_data(course_name: str):
    return get_test_by_course_name(course_name)


def _validate_correct_answers(
    allow_multiple: int,
    is_a_correct: int,
    is_b_correct: int,
    is_c_correct: int,
    is_d_correct: int,
):
    total_correct = is_a_correct + is_b_correct + is_c_correct + is_d_correct

    if total_correct == 0:
        return False

    if not allow_multiple and total_correct != 1:
        return False

    return True


def add_new_test_question(
    course_name: str,
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
    course_row = get_course_by_slug(course_name)
    if not course_row:
        return False

    if not _validate_correct_answers(
        allow_multiple,
        is_a_correct,
        is_b_correct,
        is_c_correct,
        is_d_correct,
    ):
        return False

    create_test_question(
        course_id=course_row["id"],
        question=question.strip(),
        option_a=option_a.strip(),
        option_b=option_b.strip(),
        option_c=option_c.strip(),
        option_d=option_d.strip(),
        allow_multiple=allow_multiple,
        is_a_correct=is_a_correct,
        is_b_correct=is_b_correct,
        is_c_correct=is_c_correct,
        is_d_correct=is_d_correct,
        sort_order=sort_order,
    )
    return True


def save_test_question(
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
    if not _validate_correct_answers(
        allow_multiple,
        is_a_correct,
        is_b_correct,
        is_c_correct,
        is_d_correct,
    ):
        return False

    update_test_question(
        question_id=question_id,
        question=question.strip(),
        option_a=option_a.strip(),
        option_b=option_b.strip(),
        option_c=option_c.strip(),
        option_d=option_d.strip(),
        allow_multiple=allow_multiple,
        is_a_correct=is_a_correct,
        is_b_correct=is_b_correct,
        is_c_correct=is_c_correct,
        is_d_correct=is_d_correct,
        sort_order=sort_order,
    )
    return True


def remove_test_question(question_id: int):
    delete_test_question(question_id)
    return True