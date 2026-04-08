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

    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN page_title TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE courses ADD COLUMN page_subtitle TEXT")
    except sqlite3.OperationalError:
        pass

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            allow_multiple INTEGER NOT NULL DEFAULT 0,
            is_a_correct INTEGER NOT NULL DEFAULT 0,
            is_b_correct INTEGER NOT NULL DEFAULT 0,
            is_c_correct INTEGER NOT NULL DEFAULT 0,
            is_d_correct INTEGER NOT NULL DEFAULT 0,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        )
    """)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            reset_code TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

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
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS home_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content_html TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.executemany("""
        INSERT OR IGNORE INTO courses (slug, title, description, content_file)
        VALUES (?, ?, ?, ?)
    """, courses_data)

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
            'Цей веб-сайт створений як навчальна платформа для студентів, які хочуть вивчати програмування з нуля. Тут зібрані базові курси з популярних мов програмування, які дозволяють поступово перейти від простих тем до більш складних.',
            'Основна мета сайту — допомогти студентам швидко розібратись у фундаментальних поняттях програмування та отримати практичні навички, необхідні для подальшого розвитку в IT-сфері.',

            'Кому підходить цей сайт',
            'Студентам, які тільки починають вивчати програмування',
            'Тим, хто хоче змінити сферу діяльності і перейти в IT',
            'Учням, які хочуть отримати додаткову практику',
            'Новачкам, які хочуть зрозуміти основи веб-розробки',

            'Що є на сайті',
            'Курси з програмування (C++, C#, Python, Java, JavaScript, HTML/CSS, PHP, SQL)',
            'Пояснення теорії простими словами',
            'Приклади коду для кожної теми',
            'Практичні завдання для закріплення знань',
            'Тести для перевірки рівня знань',

            'Про коледж',
            'Дрогобицький механіко-технологічний коледж є одним із провідних навчальних закладів, який готує спеціалістів у сфері технологій, програмування та механіки.',
            'Коледж надає сучасну освіту, поєднуючи теоретичні знання з практичними навичками, що дозволяє студентам бути конкурентоспроможними на ринку праці.',

            'Хто створив цей сайт',
            'Сайт розроблений студентом коледжу в рамках навчального проєкту. Метою створення було закріплення знань у веб-розробці та створення корисного ресурсу для інших студентів.',

            'Звідки навички',
            'Під час розробки сайту були використані знання з HTML, CSS та основ програмування, отримані під час навчання, а також самостійного вивчення сучасних технологій.',
            'Проєкт включає роботу з версткою, структурою сайту, стилями, логікою курсів та організацією навчального матеріалу.',

            'Чому цей проєкт важливий',
            'Сайт є не лише навчальним проєктом, а й корисним інструментом для студентів, які хочуть розпочати свій шлях у програмуванні.',
            'Він дозволяє систематизувати знання, отримати практику та краще зрозуміти, як працюють реальні веб-застосунки.'
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM home_blocks")
    blocks_count = cursor.fetchone()[0]

    if blocks_count == 0:
        cursor.execute("SELECT * FROM site_content WHERE id = 1")
        row = cursor.fetchone()

        if row:
            blocks_data = [
                {
                    "title": row[3],
                    "content_html": f"<p>{row[4]}</p><p>{row[5]}</p>",
                    "sort_order": 1,
                },
                {
                    "title": row[6],
                    "content_html": (
                        f"<ul>"
                        f"<li>{row[7]}</li>"
                        f"<li>{row[8]}</li>"
                        f"<li>{row[9]}</li>"
                        f"<li>{row[10]}</li>"
                        f"</ul>"
                    ),
                    "sort_order": 2,
                },
                {
                    "title": row[11],
                    "content_html": (
                        f"<ul>"
                        f"<li>{row[12]}</li>"
                        f"<li>{row[13]}</li>"
                        f"<li>{row[14]}</li>"
                        f"<li>{row[15]}</li>"
                        f"<li>{row[16]}</li>"
                        f"</ul>"
                    ),
                    "sort_order": 3,
                },
                {
                    "title": row[17],
                    "content_html": f"<p>{row[18]}</p><p>{row[19]}</p>",
                    "sort_order": 4,
                },
                {
                    "title": row[20],
                    "content_html": f"<p>{row[21]}</p>",
                    "sort_order": 5,
                },
                {
                    "title": row[22],
                    "content_html": f"<p>{row[23]}</p><p>{row[24]}</p>",
                    "sort_order": 6,
                },
                {
                    "title": row[25],
                    "content_html": f"<p>{row[26]}</p><p>{row[27]}</p>",
                    "sort_order": 7,
                },
            ]

            for block in blocks_data:
                cursor.execute(
                    """
                    INSERT INTO home_blocks (title, content_html, sort_order)
                    VALUES (?, ?, ?)
                    """,
                    (block["title"], block["content_html"], block["sort_order"]),
                )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    db_path = Path(DB_NAME).resolve()
    print(f"База даних створена або оновлена: {db_path}")