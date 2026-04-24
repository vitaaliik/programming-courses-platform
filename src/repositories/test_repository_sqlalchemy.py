from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.test_question import TestQuestion
from src.models.test_result import TestResult


class TestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_course_by_slug(self, course_name: str) -> Course | None:
        return self.db.query(Course).filter(Course.slug == course_name).first()

    def get_questions_by_course_id(self, course_id: int) -> list[TestQuestion]:
        return (
            self.db.query(TestQuestion)
            .filter(TestQuestion.course_id == course_id)
            .order_by(TestQuestion.sort_order.asc(), TestQuestion.id.asc())
            .all()
        )

    def save_test_result(
        self,
        user_id: int,
        course_id: int,
        score: int,
        total: int,
    ) -> None:
        result = TestResult(
            user_id=user_id,
            course_id=course_id,
            score=score,
            total=total,
        )

        self.db.add(result)
        self.db.commit()

    def create_question(
        self,
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
    ) -> None:
        test_question = TestQuestion(
            course_id=course_id,
            question=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            allow_multiple=allow_multiple,
            is_a_correct=is_a_correct,
            is_b_correct=is_b_correct,
            is_c_correct=is_c_correct,
            is_d_correct=is_d_correct,
            sort_order=sort_order,
        )

        self.db.add(test_question)
        self.db.commit()

    def update_question(
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
    ) -> None:
        test_question = (
            self.db.query(TestQuestion)
            .filter(TestQuestion.id == question_id)
            .first()
        )

        if not test_question:
            return

        test_question.question = question
        test_question.option_a = option_a
        test_question.option_b = option_b
        test_question.option_c = option_c
        test_question.option_d = option_d
        test_question.allow_multiple = allow_multiple
        test_question.is_a_correct = is_a_correct
        test_question.is_b_correct = is_b_correct
        test_question.is_c_correct = is_c_correct
        test_question.is_d_correct = is_d_correct
        test_question.sort_order = sort_order

        self.db.commit()

    def delete_question(self, question_id: int) -> None:
        (
            self.db.query(TestQuestion)
            .filter(TestQuestion.id == question_id)
            .delete()
        )
        self.db.commit()