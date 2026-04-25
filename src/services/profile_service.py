from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException, NotFoundException, ValidationException
from src.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def get_profile_data(self, user_id: int):
        user = self.repository.get_user(user_id)

        if not user:
            raise NotFoundException("Користувача не знайдено.")

        results = self.repository.get_user_results(user_id)
        total_tests = len(results)

        if total_tests > 0:
            avg_score = sum((r["score"] / r["total"]) * 100 for r in results) / total_tests
            best_score = max((r["score"] / r["total"]) * 100 for r in results)
        else:
            avg_score = 0
            best_score = 0

        total_courses = self.repository.get_total_courses()
        completed_courses = len(set(r["title"] for r in results))

        progress_percent = (
            round((completed_courses / total_courses) * 100, 1)
            if total_courses > 0
            else 0
        )

        return {
            "profile_user": {
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
            },
            "results": results,
            "recent_results": results[:4],
            "total_tests": total_tests,
            "avg_score": round(avg_score, 1),
            "best_score": round(best_score, 1),
            "completed_courses": completed_courses,
            "total_courses": total_courses,
            "progress_percent": progress_percent,
        }

    def update_username(self, user_id: int, new_username: str):
        new_username = new_username.strip()

        if not new_username:
            raise ValidationException("Нікнейм не може бути порожнім.")

        if len(new_username) < 2:
            raise ValidationException("Нікнейм має містити щонайменше 2 символи.")

        if len(new_username) > 30:
            raise ValidationException("Нікнейм занадто довгий. Максимум 30 символів.")

        try:
            user = self.repository.get_user(user_id)

            if not user:
                raise NotFoundException("Користувача не знайдено.")

            self.repository.update_username(user_id, new_username)
            self.repository.db.commit()
            return True

        except (NotFoundException, ValidationException):
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити нікнейм") from exc