import sqlite3
from pathlib import Path

DB_NAME = "database.db"

courses_data = [
    ("cpp", "C++", "Курс з основ C++", "cpp.html"),
    ("csharp", "C#", "Курс з основ C#", "csharp.html"),
    ("delphi", "Delphi", "Курс з основ Delphi", "delphi.html"),
    ("python", "Python", "Курс з основ Python", "python.html"),
    ("java", "Java", "Курс з основ Java", "java.html"),
    ("javascript", "JavaScript", "Курс з основ JavaScript", "javascript.html"),
    ("htmlcss", "HTML/CSS", "Курс з основ HTML та CSS", "htmlcss.html"),
    ("php", "PHP", "Курс з основ PHP", "php.html"),
    ("sql", "SQL", "Курс з основ SQL", "sql.html"),
]


def init_db() -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # USERS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # COURSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT,
            content_file TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Додаємо колонки якщо їх нема
    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN page_title TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN page_subtitle TEXT")
    except sqlite3.OperationalError:
        pass

    # COURSE SECTIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content_html TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        )
    """)

    # TEST RESULTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            passed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        )
    """)

    # PASSWORD RESET
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            reset_code TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # SITE CONTENT
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS site_content (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            hero_title TEXT NOT NULL,
            hero_subtitle TEXT NOT NULL,

            about_title TEXT NOT NULL,
            about_text_1 TEXT NOT NULL,
            about_text_2 TEXT NOT NULL,

            audience_title TEXT NOT NULL,
            audience_item_1 TEXT NOT NULL,
            audience_item_2 TEXT NOT NULL,
            audience_item_3 TEXT NOT NULL,
            audience_item_4 TEXT NOT NULL,

            features_title TEXT NOT NULL,
            features_item_1 TEXT NOT NULL,
            features_item_2 TEXT NOT NULL,
            features_item_3 TEXT NOT NULL,
            features_item_4 TEXT NOT NULL,
            features_item_5 TEXT NOT NULL,

            college_title TEXT NOT NULL,
            college_text_1 TEXT NOT NULL,
            college_text_2 TEXT NOT NULL,

            creator_title TEXT NOT NULL,
            creator_text TEXT NOT NULL,

            skills_title TEXT NOT NULL,
            skills_text_1 TEXT NOT NULL,
            skills_text_2 TEXT NOT NULL,

            importance_title TEXT NOT NULL,
            importance_text_1 TEXT NOT NULL,
            importance_text_2 TEXT NOT NULL
        )
    """)

    # COURSES INSERT
    cursor.executemany("""
        INSERT OR IGNORE INTO courses (slug, title, description, content_file)
        VALUES (?, ?, ?, ?)
    """, courses_data)

    # SITE CONTENT DEFAULT
    cursor.execute("""
        INSERT OR IGNORE INTO site_content (
            id,
            hero_title,
            hero_subtitle,

            about_title,
            about_text_1,
            about_text_2,

            audience_title,
            audience_item_1,
            audience_item_2,
            audience_item_3,
            audience_item_4,

            features_title,
            features_item_1,
            features_item_2,
            features_item_3,
            features_item_4,
            features_item_5,

            college_title,
            college_text_1,
            college_text_2,

            creator_title,
            creator_text,

            skills_title,
            skills_text_1,
            skills_text_2,

            importance_title,
            importance_text_1,
            importance_text_2
        )
        VALUES (
            1,
            'Курси програмування',
            'Навчальна платформа для вивчення програмування від основ до практики',

            'Про сайт',
            'Навчальна платформа для студентів...',
            'Основна мета — навчити програмуванню.',

            'Кому підходить цей сайт',
            'Студентам',
            'Новачкам',
            'Тим хто переходить в IT',
            'Учням',

            'Що є на сайті',
            'Курси',
            'Теорія',
            'Практика',
            'Тести',
            'Приклади',

            'Про коледж',
            'Коледж опис',
            'Освіта',

            'Хто створив цей сайт',
            'Студент',

            'Звідки навички',
            'Навчання',
            'Практика',

            'Чому це важливо',
            'Дає знання',
            'Дає практику'
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    db_path = Path(DB_NAME).resolve()
    print(f"База даних створена або оновлена: {db_path}")