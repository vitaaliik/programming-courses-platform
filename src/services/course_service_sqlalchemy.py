from src.repositories.course_repository_sqlalchemy import (
    get_all_courses_sa,
    get_course_by_slug_sa,
)


def get_all_courses_via_sqlalchemy(db):
    return get_all_courses_sa(db)


def get_course_by_slug_via_sqlalchemy(db, slug: str):
    return get_course_by_slug_sa(db, slug)