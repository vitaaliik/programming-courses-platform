from sqlalchemy import text
from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.course_section import CourseSection


class CourseContentRepository:
    def __init__(self, db: Session):
        self.db = db

    def _course_to_dict(self, course: Course) -> dict:
        return {
            "id": course.id,
            "slug": course.slug,
            "title": course.title,
            "description": course.description,
            "content_file": course.content_file,
            "page_title": course.page_title,
            "page_subtitle": course.page_subtitle,
        }

    def _section_to_dict(self, section: CourseSection) -> dict:
        return {
            "id": section.id,
            "course_id": section.course_id,
            "title": section.title,
            "content_html": section.content_html,
            "sort_order": section.sort_order,
            "created_at": section.created_at,
        }

    def get_course_by_slug(self, slug: str) -> dict | None:
        course = self.db.query(Course).filter(Course.slug == slug).first()
        return self._course_to_dict(course) if course else None

    def get_course_with_sections_by_slug(self, slug: str) -> dict | None:
        course = self.db.query(Course).filter(Course.slug == slug).first()

        if not course:
            return None

        course_dict = self._course_to_dict(course)

        sections = (
            self.db.query(CourseSection)
            .filter(CourseSection.course_id == course.id)
            .order_by(CourseSection.sort_order.asc(), CourseSection.id.asc())
            .all()
        )

        course_dict["sections"] = [self._section_to_dict(section) for section in sections]
        return course_dict

    def get_all_courses(self) -> list[dict]:
        courses = self.db.query(Course).order_by(Course.title.asc()).all()
        return [self._course_to_dict(course) for course in courses]

    def create_course(self, slug: str, title: str, description: str) -> None:
        course = Course(
            slug=slug,
            title=title,
            description=description,
            content_file=f"{slug}.html",
            page_title=f"Курс: {title}",
            page_subtitle=description,
        )

        self.db.add(course)
        self.db.flush()

    def update_course_main_info(
        self,
        course_id: int,
        page_title: str,
        page_subtitle: str,
    ) -> None:
        course = self.db.query(Course).filter(Course.id == course_id).first()

        if not course:
            return

        course.page_title = page_title
        course.page_subtitle = page_subtitle

        self.db.flush()

    def create_course_section(
        self,
        course_id: int,
        title: str,
        content_html: str,
        sort_order: int,
    ) -> None:
        section = CourseSection(
            course_id=course_id,
            title=title,
            content_html=content_html,
            sort_order=sort_order,
        )

        self.db.add(section)
        self.db.flush()

    def update_course_section(
        self,
        section_id: int,
        title: str,
        content_html: str,
        sort_order: int,
    ) -> None:
        section = self.db.query(CourseSection).filter(CourseSection.id == section_id).first()

        if not section:
            return

        section.title = title
        section.content_html = content_html
        section.sort_order = sort_order

        self.db.flush()

    def delete_course_section(self, section_id: int) -> None:
        self.db.query(CourseSection).filter(CourseSection.id == section_id).delete()
        self.db.flush()

    def delete_course_by_id(self, course_id: int) -> None:
        self.db.execute(
            text("DELETE FROM test_results WHERE course_id = :course_id"),
            {"course_id": course_id},
        )

        self.db.execute(
            text("DELETE FROM test_questions WHERE course_id = :course_id"),
            {"course_id": course_id},
        )

        self.db.query(CourseSection).filter(CourseSection.course_id == course_id).delete()

        self.db.query(Course).filter(Course.id == course_id).delete()

        self.db.flush()