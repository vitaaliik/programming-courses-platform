from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException, NotFoundException, ValidationException
from src.models.test_question import TestQuestion
from src.repositories.test_repository import TestRepository


class TestService:
    def __init__(self, repository: TestRepository):
        self.repository = repository

    def _extract_correct_options(self, question: TestQuestion) -> list[str]:
        correct_options = []

        if question.is_a_correct:
            correct_options.append(question.option_a)
        if question.is_b_correct:
            correct_options.append(question.option_b)
        if question.is_c_correct:
            correct_options.append(question.option_c)
        if question.is_d_correct:
            correct_options.append(question.option_d)

        return correct_options

    def _question_to_dict(self, question: TestQuestion) -> dict:
        return {
            "id": f"q{question.id}",
            "db_id": question.id,
            "question": question.question,
            "options": [
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
            ],
            "allow_multiple": bool(question.allow_multiple),
            "correct_options": self._extract_correct_options(question),
            "sort_order": question.sort_order,
            "is_a_correct": question.is_a_correct,
            "is_b_correct": question.is_b_correct,
            "is_c_correct": question.is_c_correct,
            "is_d_correct": question.is_d_correct,
        }

    def get_test_by_course_name(self, course_name: str):
        course = self.repository.get_course_by_slug(course_name)

        if not course:
            raise NotFoundException("Тест для цього курсу не знайдено.")

        questions = self.repository.get_questions_by_course_id(course.id)

        return {
            "title": f"Тест: {course.title}",
            "course_id": course.id,
            "questions": [self._question_to_dict(question) for question in questions],
        }

    def calculate_test_result(self, form, questions):
        score = 0
        total = len(questions)
        detailed_results = []

        for question in questions:
            user_answers = form.getlist(question["id"])
            correct_answers = question["correct_options"]
            is_correct = set(user_answers) == set(correct_answers)

            if is_correct:
                score += 1

            detailed_results.append(
                {
                    "question": question["question"],
                    "user_answer": ", ".join(user_answers) if user_answers else "Не вибрано",
                    "correct_answer": ", ".join(correct_answers),
                    "is_correct": is_correct,
                }
            )

        return score, total, detailed_results

    def save_result_if_logged_in(self, user_id: int | None, course_name: str, score: int, total: int):
        if not user_id:
            return

        try:
            course = self.repository.get_course_by_slug(course_name)

            if not course:
                raise NotFoundException("Курс не знайдено.")

            self.repository.save_test_result(user_id, course.id, score, total)
            self.repository.db.commit()

        except NotFoundException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося зберегти результат тесту") from exc

    def get_test_editor_data(self, course_name: str):
        return self.get_test_by_course_name(course_name)

    def _validate_correct_answers(
        self,
        allow_multiple: int,
        is_a_correct: int,
        is_b_correct: int,
        is_c_correct: int,
        is_d_correct: int,
    ):
        total_correct = is_a_correct + is_b_correct + is_c_correct + is_d_correct

        if total_correct == 0:
            raise ValidationException("Потрібно вибрати хоча б одну правильну відповідь.")

        if not allow_multiple and total_correct != 1:
            raise ValidationException("Для одного вибору має бути тільки одна правильна відповідь.")

    def add_new_test_question(
        self,
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
        try:
            course = self.repository.get_course_by_slug(course_name)

            if not course:
                raise NotFoundException("Курс не знайдено.")

            self._validate_correct_answers(
                allow_multiple,
                is_a_correct,
                is_b_correct,
                is_c_correct,
                is_d_correct,
            )

            self.repository.create_question(
                course_id=course.id,
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
            self.repository.db.commit()
            return True

        except (NotFoundException, ValidationException):
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося додати питання") from exc

    def save_test_question(
        self,
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
        try:
            self._validate_correct_answers(
                allow_multiple,
                is_a_correct,
                is_b_correct,
                is_c_correct,
                is_d_correct,
            )

            self.repository.update_question(
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
            self.repository.db.commit()
            return True

        except ValidationException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити питання") from exc

    def remove_test_question(self, question_id: int):
        try:
            self.repository.delete_question(question_id)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося видалити питання") from exc