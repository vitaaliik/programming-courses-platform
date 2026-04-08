from src.core.database import get_db_connection
from src.data.tests_data import TESTS


EXTRA_QUESTIONS = {
    "cpp": [
        {
            "question": "Який символ використовується для завершення більшості інструкцій у C++?",
            "options": [";", ":", ".", ","],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що робить оператор if у C++?",
            "options": ["Описує масив", "Перевіряє умову", "Створює клас", "Підключає бібліотеку"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Який контейнер часто використовують для тексту в C++?",
            "options": ["bool", "std::string", "float", "vector<int>"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке масив у C++?",
            "options": ["Одна змінна типу bool", "Набір значень одного типу", "Тільки текст", "Коментар"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Які з цього є базовими конструкціями C++?",
            "options": ["if", "for", "SELECT", "while"],
            "correct_indexes": [0, 1, 3],
            "allow_multiple": 1,
        },
    ],
    "csharp": [
        {
            "question": "На якій платформі найтісніше пов’язаний C#?",
            "options": [".NET", "Photoshop", "MySQL Workbench", "HTML5"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Який тип використовується для логічного значення у C#?",
            "options": ["logic", "bool", "bit", "yesno"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке клас у C#?",
            "options": ["Стиль сторінки", "Шаблон для створення об’єктів", "Запит до БД", "Коментар"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Яке ключове слово часто використовують для автоматичного визначення типу?",
            "options": ["auto", "var", "dynamiclet", "typeofvalue"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього є типовими конструкціями C#?",
            "options": ["class", "namespace", "SELECT", "Main()"],
            "correct_indexes": [0, 1, 3],
            "allow_multiple": 1,
        },
    ],
    "delphi": [
        {
            "question": "Який оператор присвоєння використовується в Delphi?",
            "options": ["=", ":=", "->", "=="],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Який тип даних для тексту в Delphi?",
            "options": ["String", "Text[]", "Word", "Memo"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке TEdit у Delphi?",
            "options": ["Кнопка", "Поле вводу", "Зображення", "Таблиця"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Яка команда виводить текст у консоль Delphi?",
            "options": ["Println", "Console.Write", "Writeln", "echo"],
            "correct_indexes": [2],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього часто є компонентами Delphi?",
            "options": ["TButton", "TLabel", "TEdit", "JOIN"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "python": [
        {
            "question": "Яка структура даних у Python зберігає впорядкований список елементів?",
            "options": ["set", "list", "dict", "bool"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що робить функція len()?",
            "options": ["Друкує текст", "Рахує довжину", "Створює цикл", "Видаляє файл"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Яке ключове слово використовується для умови в Python?",
            "options": ["if", "when", "case", "switch"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що означає True у Python?",
            "options": ["Рядок", "Логічне істинне значення", "Число", "Коментар"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього є базовими типами Python?",
            "options": ["str", "int", "bool", "JOIN"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "java": [
        {
            "question": "Що таке JVM?",
            "options": ["Java Virtual Machine", "Java Visual Method", "Joint Variable Model", "JSON View Mode"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Яке слово використовують для створення об’єкта в Java?",
            "options": ["make", "new", "create", "object"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке String у Java?",
            "options": ["Тип для тексту", "Тип циклу", "Масив стилів", "Метод друку"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Яке слово фіксує незмінне значення в Java?",
            "options": ["const", "final", "fixed", "static"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього пов’язане з Java?",
            "options": ["class", "object", "JVM", "margin"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "javascript": [
        {
            "question": "Який метод шукає елемент у DOM за id?",
            "options": ["getElementById()", "findNode()", "queryPage()", "selectCss()"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що робить alert()?",
            "options": ["Змінює CSS", "Показує повідомлення", "Створює масив", "Завантажує базу"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Який тип даних означає логічне значення у JS?",
            "options": ["bool", "boolean", "logic", "truth"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Для чого використовують addEventListener()?",
            "options": ["Для підключення SQL", "Для обробки подій", "Для створення стилів", "Для імпорту Python"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього пов’язане з JavaScript у браузері?",
            "options": ["DOM", "events", "console.log()", "PRIMARY KEY"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "htmlcss": [
        {
            "question": "Який тег використовується для абзацу?",
            "options": ["<p>", "<div>", "<h1>", "<spanblock>"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Яка CSS-властивість задає розмір шрифту?",
            "options": ["font-size", "text-color", "size", "font-weight"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке margin?",
            "options": ["Внутрішній відступ", "Зовнішній відступ", "Колір тексту", "Тип шрифту"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке padding?",
            "options": ["Внутрішній відступ", "Зовнішній відступ", "Тінь", "Посилання"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього належить до HTML/CSS?",
            "options": ["<a>", "color", "Flexbox", "UPDATE"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "php": [
        {
            "question": "Який метод форми зазвичай використовують для відправки конфіденційних даних?",
            "options": ["GET", "POST", "SHOW", "LOAD"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке сесія в PHP?",
            "options": ["Стиль сторінки", "Збереження даних користувача між запитами", "Тип циклу", "Компілятор"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Яка функція часто використовується для підключення до MySQL через PDO?",
            "options": ["new PDO()", "mysql_start()", "db.open()", "connect_sql()"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке $_GET?",
            "options": ["Масив даних GET-запиту", "Функція циклу", "Тип стилю", "Клас PHP"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього характерне для PHP?",
            "options": ["$_POST", "echo", "$name", "JOIN"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
    "sql": [
        {
            "question": "Яка команда створює таблицю?",
            "options": ["MAKE TABLE", "CREATE TABLE", "NEW TABLE", "TABLE ADD"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що таке PRIMARY KEY?",
            "options": ["Головний унікальний ключ", "Колір таблиці", "Тип циклу", "Фільтр запиту"],
            "correct_indexes": [0],
            "allow_multiple": 0,
        },
        {
            "question": "Яка команда змінює існуючі записи?",
            "options": ["CHANGE", "MODIFY ROW", "UPDATE", "REWRITE"],
            "correct_indexes": [2],
            "allow_multiple": 0,
        },
        {
            "question": "Яка команда видаляє записи?",
            "options": ["DROP ROW", "DELETE", "REMOVE ALL", "ERASE"],
            "correct_indexes": [1],
            "allow_multiple": 0,
        },
        {
            "question": "Що з цього належить до SQL?",
            "options": ["SELECT", "WHERE", "JOIN", "padding"],
            "correct_indexes": [0, 1, 2],
            "allow_multiple": 1,
        },
    ],
}


def convert_old_question(question):
    correct_indexes = [question["options"].index(question["correct"])]
    return {
        "question": question["question"],
        "options": question["options"],
        "correct_indexes": correct_indexes,
        "allow_multiple": 0,
    }


def main():
    conn = get_db_connection()
    cursor = conn.cursor()

    for course_slug, test_data in TESTS.items():
        cursor.execute("SELECT id FROM courses WHERE slug = ?", (course_slug,))
        course = cursor.fetchone()

        if not course:
            print(f"[SKIP] Курс {course_slug} не знайдено")
            continue

        course_id = course["id"]

        cursor.execute("DELETE FROM test_questions WHERE course_id = ?", (course_id,))

        base_questions = [convert_old_question(q) for q in test_data["questions"]]
        combined_questions = base_questions + EXTRA_QUESTIONS.get(course_slug, [])

        for index, question in enumerate(combined_questions, start=1):
            options = question["options"]
            correct_indexes = question["correct_indexes"]

            is_a_correct = 1 if 0 in correct_indexes else 0
            is_b_correct = 1 if 1 in correct_indexes else 0
            is_c_correct = 1 if 2 in correct_indexes else 0
            is_d_correct = 1 if 3 in correct_indexes else 0

            cursor.execute(
                """
                INSERT INTO test_questions (
                    course_id,
                    question,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    allow_multiple,
                    is_a_correct,
                    is_b_correct,
                    is_c_correct,
                    is_d_correct,
                    sort_order
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    course_id,
                    question["question"],
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    question["allow_multiple"],
                    is_a_correct,
                    is_b_correct,
                    is_c_correct,
                    is_d_correct,
                    index,
                ),
            )

        print(f"[OK] {course_slug}: додано {len(combined_questions)} питань")

    conn.commit()
    conn.close()
    print("Тести успішно імпортовані в БД.")
    

if __name__ == "__main__":
    main()