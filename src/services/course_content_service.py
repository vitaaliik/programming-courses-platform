from sqlalchemy.exc import SQLAlchemyError

from src.repositories.course_content_repository import CourseContentRepository


class CourseContentService:
    def __init__(self, repository: CourseContentRepository):
        self.repository = repository

    def get_course_page_data(self, slug: str):
        return self.repository.get_course_with_sections_by_slug(slug)

    def get_courses_for_admin(self):
        return self.repository.get_all_courses()

    def get_courses_for_page(self):
        return self.repository.get_all_courses()

    def get_course_editor_data(self, slug: str):
        return self.repository.get_course_with_sections_by_slug(slug)

    def save_course_main_info(self, slug: str, page_title: str, page_subtitle: str):
        try:
            course = self.repository.get_course_with_sections_by_slug(slug)
            if not course:
                return False

            self.repository.update_course_main_info(
                course_id=course["id"],
                page_title=page_title.strip(),
                page_subtitle=page_subtitle.strip(),
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def add_new_course_section(self, slug: str, title: str, content_html: str, sort_order: int):
        try:
            course = self.repository.get_course_with_sections_by_slug(slug)
            if not course:
                return False

            self.repository.create_course_section(
                course_id=course["id"],
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def save_course_section(self, section_id: int, title: str, content_html: str, sort_order: int):
        try:
            self.repository.update_course_section(
                section_id=section_id,
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def remove_course_section(self, section_id: int):
        try:
            self.repository.delete_course_section(section_id)
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def create_new_course(self, slug: str, title: str, description: str):
        slug = slug.strip().lower()
        title = title.strip()
        description = description.strip()

        if not slug or not title or not description:
            return {"ok": False, "message": "Усі поля обов'язкові."}

        try:
            existing = self.repository.get_course_by_slug(slug)
            if existing:
                return {"ok": False, "message": "Курс із таким slug уже існує."}

            self.repository.create_course(slug, title, description)
            self.repository.db.commit()
            return {"ok": True, "message": "Новий курс успішно створено."}
        except SQLAlchemyError:
            self.repository.db.rollback()
            return {"ok": False, "message": "Помилка бази даних. Курс не створено."}

    def remove_course(self, slug: str):
        try:
            course = self.repository.get_course_by_slug(slug)
            if not course:
                return {"ok": False, "message": "Курс не знайдено."}

            self.repository.delete_course_by_id(course["id"])
            self.repository.db.commit()
            return {"ok": True, "message": "Курс видалено."}
        except SQLAlchemyError:
            self.repository.db.rollback()
            return {"ok": False, "message": "Помилка бази даних. Курс не видалено."}