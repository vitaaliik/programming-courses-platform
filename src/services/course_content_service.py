from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import (
    AppException,
    DatabaseException,
    NotFoundException,
    ValidationException,
)
from src.repositories.course_content_repository import CourseContentRepository


class CourseContentService:
    def __init__(self, repository: CourseContentRepository):
        self.repository = repository

    def get_course_page_data(self, slug: str):
        course = self.repository.get_course_with_sections_by_slug(slug)

        if not course:
            raise NotFoundException("Курс не знайдено.")

        return course

    def get_courses_for_admin(self):
        return self.repository.get_all_courses()

    def get_courses_for_page(self):
        return self.repository.get_all_courses()

    def get_course_editor_data(self, slug: str):
        course = self.repository.get_course_with_sections_by_slug(slug)

        if not course:
            raise NotFoundException("Курс не знайдено.")

        return course

    def save_course_main_info(self, slug: str, page_title: str, page_subtitle: str):
        try:
            course = self.repository.get_course_with_sections_by_slug(slug)

            if not course:
                raise NotFoundException("Курс не знайдено.")

            self.repository.update_course_main_info(
                course_id=course["id"],
                page_title=page_title.strip(),
                page_subtitle=page_subtitle.strip(),
            )
            self.repository.db.commit()
            return True

        except AppException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити основну інформацію курсу") from exc

    def add_new_course_section(self, slug: str, title: str, content_html: str, sort_order: int):
        if not title.strip():
            raise ValidationException("Назва секції не може бути порожньою.")

        try:
            course = self.repository.get_course_with_sections_by_slug(slug)

            if not course:
                raise NotFoundException("Курс не знайдено.")

            self.repository.create_course_section(
                course_id=course["id"],
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True

        except AppException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося додати секцію курсу") from exc

    def save_course_section(self, section_id: int, title: str, content_html: str, sort_order: int):
        if not title.strip():
            raise ValidationException("Назва секції не може бути порожньою.")

        try:
            self.repository.update_course_section(
                section_id=section_id,
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити секцію курсу") from exc

    def remove_course_section(self, section_id: int):
        try:
            self.repository.delete_course_section(section_id)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося видалити секцію курсу") from exc

    def create_new_course(self, slug: str, title: str, description: str):
        slug = slug.strip().lower()
        title = title.strip()
        description = description.strip()

        if not slug or not title or not description:
            raise ValidationException("Усі поля обов'язкові.")

        try:
            existing = self.repository.get_course_by_slug(slug)

            if existing:
                raise ValidationException("Курс із таким slug уже існує.")

            self.repository.create_course(slug, title, description)
            self.repository.db.commit()

            return {"ok": True, "message": "Новий курс успішно створено."}

        except AppException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося створити курс") from exc

    def remove_course(self, slug: str):
        try:
            course = self.repository.get_course_by_slug(slug)

            if not course:
                raise NotFoundException("Курс не знайдено.")

            self.repository.delete_course_by_id(course["id"])
            self.repository.db.commit()

            return {"ok": True, "message": "Курс видалено."}

        except AppException:
            self.repository.db.rollback()
            raise

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося видалити курс") from exc