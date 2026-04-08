from pathlib import Path
import sqlite3
from bs4 import BeautifulSoup

DB_NAME = "database.db"

# Тут вкажи свої реальні файли з templates/
COURSE_FILES = {
    "cpp": "templates/cpp.html",
    "csharp": "templates/csharp.html",
    "delphi": "templates/delphi.html",
    "htmlcss": "templates/htmlcss.html",
    "java": "templates/java.html",
    "javascript": "templates/javascript.html",
    "php": "templates/php.html",
    "python": "templates/python.html",
    "sql": "templates/sql.html",
}

# C++ вже перенесений, тому його тут не чіпаємо


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def clean_inner_html(section_tag):
    """
    Забираємо з секції тільки h3, а решту залишаємо як HTML-контент.
    """
    section_copy = BeautifulSoup(str(section_tag), "html.parser")
    root = section_copy.find("section")

    h3 = root.find("h3")
    if h3:
        h3.decompose()

    return "".join(str(child) for child in root.contents).strip()


def parse_course_file(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    header = soup.find("div", class_="course-header")
    if not header:
        raise ValueError(f"У файлі {file_path} не знайдено .course-header")

    h2 = header.find("h2")
    p = header.find("p")

    page_title = h2.get_text(strip=True) if h2 else ""
    page_subtitle = p.get_text(" ", strip=True) if p else ""

    sections = []
    section_tags = soup.find_all("section", class_="course-section")

    for index, section_tag in enumerate(section_tags, start=1):
        h3 = section_tag.find("h3")
        title = h3.get_text(" ", strip=True) if h3 else f"Секція {index}"
        content_html = clean_inner_html(section_tag)

        sections.append(
            {
                "title": title,
                "content_html": content_html,
                "sort_order": index,
            }
        )

    return page_title, page_subtitle, sections


def import_course(slug: str, file_path: str):
    page_title, page_subtitle, sections = parse_course_file(file_path)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM courses WHERE slug = ?", (slug,))
    course = cursor.fetchone()

    if not course:
        conn.close()
        raise ValueError(f"Курс зі slug='{slug}' не знайдено в таблиці courses")

    course_id = course["id"]

    # Оновлюємо page_title / page_subtitle
    cursor.execute(
        """
        UPDATE courses
        SET page_title = ?, page_subtitle = ?
        WHERE id = ?
        """,
        (page_title, page_subtitle, course_id),
    )

    # Видаляємо старі секції цього курсу
    cursor.execute(
        "DELETE FROM course_sections WHERE course_id = ?",
        (course_id,),
    )

    # Вставляємо нові
    cursor.executemany(
        """
        INSERT INTO course_sections (course_id, title, content_html, sort_order)
        VALUES (?, ?, ?, ?)
        """,
        [
            (course_id, section["title"], section["content_html"], section["sort_order"])
            for section in sections
        ],
    )

    conn.commit()
    conn.close()

    print(f"[OK] {slug}: імпортовано {len(sections)} секцій")


def main():
    for slug, file_path in COURSE_FILES.items():
        import_course(slug, file_path)

    print("Усі курси успішно імпортовано в БД.")


if __name__ == "__main__":
    main()