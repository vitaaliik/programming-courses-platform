from src.repositories.course_content_repository import (
    create_course_section,
    delete_course_section,
    get_all_courses_for_admin,
    get_course_with_sections_by_slug,
    update_course_main_info,
    update_course_section,
)


def get_course_page_data(slug: str):
    return get_course_with_sections_by_slug(slug)


def get_courses_for_admin():
    return get_all_courses_for_admin()


def get_course_editor_data(slug: str):
    return get_course_with_sections_by_slug(slug)


def save_course_main_info(slug: str, page_title: str, page_subtitle: str):
    course = get_course_with_sections_by_slug(slug)
    if not course:
        return False

    update_course_main_info(
        course_id=course["id"],
        page_title=page_title.strip(),
        page_subtitle=page_subtitle.strip(),
    )
    return True


def add_new_course_section(slug: str, title: str, content_html: str, sort_order: int):
    course = get_course_with_sections_by_slug(slug)
    if not course:
        return False

    create_course_section(
        course_id=course["id"],
        title=title.strip(),
        content_html=content_html.strip(),
        sort_order=sort_order,
    )
    return True


def save_course_section(section_id: int, title: str, content_html: str, sort_order: int):
    update_course_section(
        section_id=section_id,
        title=title.strip(),
        content_html=content_html.strip(),
        sort_order=sort_order,
    )
    return True


def remove_course_section(section_id: int):
    delete_course_section(section_id)
    return True