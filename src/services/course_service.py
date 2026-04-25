from src.repositories.course_repository import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    def get_all_courses(self):
        return self.repository.get_all()

    def get_course_by_slug(self, slug: str):
        return self.repository.get_by_slug(slug)