import os
import random
import smtplib
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super_secret_key_12345")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "database.db"

MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", "")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =========================
# Робота з базою даних
# =========================
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_site_content():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM site_content WHERE id = 1")
    content = cursor.fetchone()

    conn.close()

    return dict(content) if content else {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def render_page(request: Request, template_name: str, **context):
    base_context = {
        "request": request,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
    }
    base_context.update(context)
    return templates.TemplateResponse(template_name, base_context)


# =========================
# Email / reset helpers
# =========================
def generate_reset_code() -> str:
    return str(random.randint(100000, 999999))


def send_reset_email(receiver_email: str, code: str) -> None:
    if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_FROM:
        raise RuntimeError("Пошта не налаштована. Перевір .env")

    subject = "Код для відновлення пароля"
    body = f"""
Ваш код для відновлення пароля: {code}

Код дійсний 10 хвилин.
Якщо ви не запитували відновлення пароля, просто проігноруйте цей лист.
""".strip()

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_FROM, receiver_email, msg.as_string())


# =========================
# Дані тестів
# =========================
TESTS = {
"cpp": {
        "title": "Тест: C++",
        "questions": [
            {"id": "q1", "question": "Який тип даних у C++ використовується для цілих чисел?", "options": ["string", "int", "bool", "char"], "correct": "int"},
            {"id": "q2", "question": "Яка функція є точкою входу в програму C++?", "options": ["start()", "run()", "main()", "init()"], "correct": "main()"},
            {"id": "q3", "question": "Який оператор використовується для виведення в C++?", "options": ["<<", ">>", "::", "&&"], "correct": "<<"},
            {"id": "q4", "question": "Що означає цикл for?", "options": ["Перевірка умови", "Багаторазове повторення коду", "Оголошення змінної", "Створення функції"], "correct": "Багаторазове повторення коду"},
            {"id": "q5", "question": "Що таке функція в C++?", "options": ["Тип даних", "Окрема змінна", "Блок коду для виконання задачі", "Коментар"], "correct": "Блок коду для виконання задачі"}
        ]
    },
    "csharp": {
        "title": "Тест: C#",
        "questions": [
            {"id": "q1", "question": "Хто розробив мову C#?", "options": ["Google", "Microsoft", "Apple", "IBM"], "correct": "Microsoft"},
            {"id": "q2", "question": "Який метод є точкою входу в програму C#?", "options": ["run()", "Main()", "start()", "init()"], "correct": "Main()"},
            {"id": "q3", "question": "Який тип даних у C# використовується для цілого числа?", "options": ["string", "bool", "int", "double[]"], "correct": "int"},
            {"id": "q4", "question": "Що використовується для виведення тексту в консоль у C#?", "options": ["echo()", "Console.WriteLine()", "print()", "cout"], "correct": "Console.WriteLine()"},
            {"id": "q5", "question": "Якою є мова C#?", "options": ["Мовою розмітки", "Об'єктно-орієнтованою мовою програмування", "Базою даних", "Графічним редактором"], "correct": "Об'єктно-орієнтованою мовою програмування"}
        ]
    },
    "delphi": {
        "title": "Тест: Delphi",
        "questions": [
            {"id": "q1", "question": "На базі якої мови створено Delphi?", "options": ["Python", "Object Pascal", "Java", "C"], "correct": "Object Pascal"},
            {"id": "q2", "question": "Які ключові слова обмежують блок коду в Delphi?", "options": ["start / stop", "begin / end", "if / else", "open / close"], "correct": "begin / end"},
            {"id": "q3", "question": "Який тип даних у Delphi використовується для цілого числа?", "options": ["String", "Boolean", "Integer", "Char[]"], "correct": "Integer"},
            {"id": "q4", "question": "Який компонент у Delphi є кнопкою?", "options": ["TEdit", "TLabel", "TButton", "TMemo"], "correct": "TButton"},
            {"id": "q5", "question": "Що таке Delphi найчастіше використовує для швидкого створення інтерфейсу?", "options": ["RAD-підхід", "Тільки консоль", "SQL-запити", "Мову CSS"], "correct": "RAD-підхід"}
        ]
    },
    "python": {
        "title": "Тест: Python",
        "questions": [
            {"id": "q1", "question": "Яка функція використовується для виведення в Python?", "options": ["echo()", "print()", "cout", "write()"], "correct": "print()"},
            {"id": "q2", "question": "Який тип даних використовується для тексту?", "options": ["int", "bool", "str", "float"], "correct": "str"},
            {"id": "q3", "question": "Що в Python дуже важливе для блоків коду?", "options": ["Фігурні дужки", "Крапка з комою", "Відступи", "Коми"], "correct": "Відступи"},
            {"id": "q4", "question": "Який цикл часто використовують для проходу по списку?", "options": ["if", "for", "switch", "class"], "correct": "for"},
            {"id": "q5", "question": "Як у Python створюється функція?", "options": ["func", "function", "def", "make"], "correct": "def"}
        ]
    },
    "java": {
        "title": "Тест: Java",
        "questions": [
            {"id": "q1", "question": "Який метод є точкою входу в Java-програму?", "options": ["run()", "main()", "start()", "begin()"], "correct": "main()"},
            {"id": "q2", "question": "Який тип даних використовується для цілих чисел у Java?", "options": ["number", "integer", "int", "float"], "correct": "int"},
            {"id": "q3", "question": "Що використовується для виведення в консоль?", "options": ["print()", "System.out.println()", "echo()", "cout"], "correct": "System.out.println()"},
            {"id": "q4", "question": "Java є якою мовою?", "options": ["Тільки мовою розмітки", "Об'єктно-орієнтованою", "Графічним редактором", "Базою даних"], "correct": "Об'єктно-орієнтованою"},
            {"id": "q5", "question": "Що таке клас у Java?", "options": ["Цикл", "Файл стилів", "Шаблон для створення об'єктів", "Умова"], "correct": "Шаблон для створення об'єктів"}
        ]
    },
    "javascript": {
        "title": "Тест: JavaScript",
        "questions": [
            {"id": "q1", "question": "Де найчастіше виконується JavaScript?", "options": ["У браузері", "У Photoshop", "У SQL Server", "У Word"], "correct": "У браузері"},
            {"id": "q2", "question": "Яке ключове слово використовують для створення змінної?", "options": ["let", "echo", "int", "class"], "correct": "let"},
            {"id": "q3", "question": "Яка функція часто використовується для виведення в консоль?", "options": ["print()", "console.log()", "echo()", "write()"], "correct": "console.log()"},
            {"id": "q4", "question": "Що таке DOM?", "options": ["Мова програмування", "Структура HTML, з якою працює JavaScript", "База даних", "Тип змінної"], "correct": "Структура HTML, з якою працює JavaScript"},
            {"id": "q5", "question": "Яка подія спрацьовує при натисканні кнопки?", "options": ["onclick", "onwrite", "onloadcss", "onint"], "correct": "onclick"}
        ]
    },
    "htmlcss": {
        "title": "Тест: HTML/CSS",
        "questions": [
            {"id": "q1", "question": "HTML відповідає за що?", "options": ["Структуру сторінки", "Базу даних", "Сервер", "Мову Python"], "correct": "Структуру сторінки"},
            {"id": "q2", "question": "CSS відповідає за що?", "options": ["Стиль і вигляд", "SQL-запити", "Логіку бекенду", "Компіляцію"], "correct": "Стиль і вигляд"},
            {"id": "q3", "question": "Який тег використовується для посилання?", "options": ["<a>", "<img>", "<div>", "<p>"], "correct": "<a>"},
            {"id": "q4", "question": "Яка властивість CSS задає колір тексту?", "options": ["background", "font-size", "color", "width"], "correct": "color"},
            {"id": "q5", "question": "Що таке Flexbox?", "options": ["Інструмент для макетів", "Тип бази даних", "Мова програмування", "Тип циклу"], "correct": "Інструмент для макетів"}
        ]
    },
    "php": {
        "title": "Тест: PHP",
        "questions": [
            {"id": "q1", "question": "Де виконується PHP-код?", "options": ["У браузері", "На сервері", "У CSS", "У VS Code"], "correct": "На сервері"},
            {"id": "q2", "question": "З якого символу починається змінна в PHP?", "options": ["#", "$", "@", "%"], "correct": "$"},
            {"id": "q3", "question": "Що використовується для виведення в PHP?", "options": ["print()", "echo", "cout", "console.log"], "correct": "echo"},
            {"id": "q4", "question": "Який масив містить дані форми POST?", "options": ["$_GET", "$POST", "$_POST", "$_FORM"], "correct": "$_POST"},
            {"id": "q5", "question": "Для чого часто використовують PHP?", "options": ["Для стилів сторінки", "Для серверної логіки і роботи з базою", "Для монтажу відео", "Для створення іконок"], "correct": "Для серверної логіки і роботи з базою"}
        ]
    },
    "sql": {
        "title": "Тест: SQL",
        "questions": [
            {"id": "q1", "question": "Для чого використовується SQL?", "options": ["Для стилів сторінки", "Для роботи з базами даних", "Для анімації", "Для іконок"], "correct": "Для роботи з базами даних"},
            {"id": "q2", "question": "Яка команда вибирає дані з таблиці?", "options": ["GET", "TAKE", "SELECT", "PICK"], "correct": "SELECT"},
            {"id": "q3", "question": "Яка команда додає запис у таблицю?", "options": ["INSERT", "UPDATE", "ADDROW", "APPENDSQL"], "correct": "INSERT"},
            {"id": "q4", "question": "Для чого потрібен WHERE?", "options": ["Для фільтрації записів", "Для видалення всіх таблиць", "Для кольору тексту", "Для запуску Python"], "correct": "Для фільтрації записів"},
            {"id": "q5", "question": "Що робить JOIN?", "options": ["Об'єднує таблиці", "Фарбує сторінку", "Створює цикл", "Додає CSS"], "correct": "Об'єднує таблиці"}
        ]
    }
}


# =========================
# Звичайні сторінки сайту
# =========================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    site_content = get_site_content()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
        "site_content": site_content
    })


@app.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    return render_page(request, "courses.html")


@app.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/profile", status_code=303)
    return render_page(request, "auth.html")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/profile", status_code=303)
    return render_page(request, "login.html")


@app.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password or not confirm_password:
        return JSONResponse({"ok": False, "message": "Усі поля обов'язкові для заповнення."})

    if password != confirm_password:
        return JSONResponse({"ok": False, "message": "Паролі не співпадають."})

    if len(password) < 6:
        return JSONResponse({"ok": False, "message": "Пароль не може бути меншим за 6 символів."})

    if len(password) > 72:
        return JSONResponse({"ok": False, "message": "Пароль занадто довгий (максимум 72 символи)."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    existing_email = cursor.fetchone()

    if existing_email:
        conn.close()
        return JSONResponse({"ok": False, "message": "Така пошта вже зареєстрована."})

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, (username, email, password_hash, "user"))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    request.session["user_id"] = user_id
    request.session["username"] = username
    request.session["role"] = "user"

    return JSONResponse({"ok": True, "redirect": "/profile"})


@app.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    email = email.strip().lower()

    if not email or not password:
        return JSONResponse({"ok": False, "message": "Введіть пошту і пароль."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

    if not verify_password(password, user["password_hash"]):
        conn.close()
        return JSONResponse({"ok": False, "message": "Неправильний пароль."})

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]

    conn.close()

    if user["role"] == "admin":
        return JSONResponse({"ok": True, "redirect": "/admin"})

    return JSONResponse({"ok": True, "redirect": "/profile"})

# =========================
# Forgot password
# =========================
@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return render_page(request, "forgot_password.html")


@app.post("/forgot-password")
async def forgot_password(email: str = Form(...)):
    email = email.strip().lower()

    if not email:
        return JSONResponse({"ok": False, "message": "Введіть пошту."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return JSONResponse({"ok": False, "message": "Користувача з такою поштою не знайдено."})

    code = generate_reset_code()
    expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()

    cursor.execute("DELETE FROM password_resets WHERE email = ?", (email,))
    cursor.execute("""
        INSERT INTO password_resets (email, reset_code, expires_at)
        VALUES (?, ?, ?)
    """, (email, code, expires_at))

    conn.commit()
    conn.close()

    try:
        send_reset_email(email, code)
    except Exception as e:
        return JSONResponse({"ok": False, "message": f"Не вдалося надіслати лист: {str(e)}"})

    return JSONResponse({"ok": True, "redirect": f"/verify-code?email={email}"})


@app.get("/verify-code", response_class=HTMLResponse)
async def verify_code_page(request: Request, email: str = ""):
    return render_page(request, "verify_code.html", reset_email=email)


@app.post("/verify-code")
async def verify_code(
    email: str = Form(...),
    code: str = Form(...)
):
    email = email.strip().lower()
    code = code.strip()

    if not email or not code:
        return JSONResponse({"ok": False, "message": "Заповніть усі поля."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM password_resets
        WHERE email = ? AND reset_code = ?
        ORDER BY id DESC LIMIT 1
    """, (email, code))
    reset_row = cursor.fetchone()

    conn.close()

    if not reset_row:
        return JSONResponse({"ok": False, "message": "Неправильний код."})

    expires_at = datetime.fromisoformat(reset_row["expires_at"])
    if datetime.now() > expires_at:
        return JSONResponse({"ok": False, "message": "Час дії коду минув."})

    return JSONResponse({"ok": True, "redirect": f"/reset-password?email={email}&code={code}"})


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, email: str = "", code: str = ""):
    return render_page(request, "reset_password.html", reset_email=email, reset_code=code)


@app.post("/reset-password")
async def reset_password(
    email: str = Form(...),
    code: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    email = email.strip().lower()
    code = code.strip()

    if not email or not code or not new_password or not confirm_password:
        return JSONResponse({"ok": False, "message": "Усі поля обов'язкові."})

    if new_password != confirm_password:
        return JSONResponse({"ok": False, "message": "Паролі не співпадають."})

    if len(new_password) < 6:
        return JSONResponse({"ok": False, "message": "Пароль не може бути меншим за 6 символів."})

    if len(new_password) > 72:
        return JSONResponse({"ok": False, "message": "Пароль занадто довгий (максимум 72 символи)."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM password_resets
        WHERE email = ? AND reset_code = ?
        ORDER BY id DESC LIMIT 1
    """, (email, code))
    reset_row = cursor.fetchone()

    if not reset_row:
        conn.close()
        return JSONResponse({"ok": False, "message": "Неправильний код."})

    expires_at = datetime.fromisoformat(reset_row["expires_at"])
    if datetime.now() > expires_at:
        conn.close()
        return JSONResponse({"ok": False, "message": "Час дії коду минув."})

    password_hash = hash_password(new_password)

    cursor.execute("""
        UPDATE users
        SET password_hash = ?
        WHERE email = ?
    """, (password_hash, email))

    cursor.execute("DELETE FROM password_resets WHERE email = ?", (email,))

    conn.commit()
    conn.close()

    return JSONResponse({"ok": True, "redirect": "/login"})


@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, email, created_at
        FROM users
        WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    user = dict(user)

    cursor.execute("""
        SELECT test_results.score, test_results.total, test_results.passed_at, courses.title, courses.slug
        FROM test_results
        JOIN courses ON test_results.course_id = courses.id
        WHERE test_results.user_id = ?
        ORDER BY test_results.passed_at DESC
    """, (user_id,))
    results = cursor.fetchall()

    results = [dict(r) for r in results]

    total_tests = len(results)

    if total_tests > 0:
        avg_score = sum((r["score"] / r["total"]) * 100 for r in results) / total_tests
        best_score = max((r["score"] / r["total"]) * 100 for r in results)
    else:
        avg_score = 0
        best_score = 0

    cursor.execute("SELECT COUNT(*) as total FROM courses")
    total_courses = cursor.fetchone()["total"]

    completed_courses = len(set(r["title"] for r in results))
    progress_percent = round((completed_courses / total_courses) * 100, 1) if total_courses > 0 else 0

    recent_results = results[:4]

    conn.close()

    return render_page(
        request,
        "profile.html",
        profile_user=user,
        results=results,
        recent_results=recent_results,
        total_tests=total_tests,
        avg_score=round(avg_score, 1),
        best_score=round(best_score, 1),
        completed_courses=completed_courses,
        total_courses=total_courses,
        progress_percent=progress_percent
    )

@app.post("/profile/update-username")
async def update_username(
    request: Request,
    new_username: str = Form(...)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return JSONResponse({"ok": False, "message": "Спочатку увійдіть у систему."})

    new_username = new_username.strip()

    if not new_username:
        return JSONResponse({"ok": False, "message": "Нікнейм не може бути порожнім."})

    if len(new_username) < 2:
        return JSONResponse({"ok": False, "message": "Нікнейм має містити щонайменше 2 символи."})

    if len(new_username) > 30:
        return JSONResponse({"ok": False, "message": "Нікнейм занадто довгий (максимум 30 символів)."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET username = ?
        WHERE id = ?
    """, (new_username, user_id))

    conn.commit()
    conn.close()

    request.session["username"] = new_username

    return JSONResponse({"ok": True, "message": "Нікнейм успішно оновлено."})

@app.get("/logout")
async def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/cpp", response_class=HTMLResponse)
async def cpp_page(request: Request):
    return render_page(request, "cpp.html")


@app.get("/csharp", response_class=HTMLResponse)
async def csharp_page(request: Request):
    return render_page(request, "csharp.html")


@app.get("/delphi", response_class=HTMLResponse)
async def delphi_page(request: Request):
    return render_page(request, "delphi.html")


@app.get("/python", response_class=HTMLResponse)
async def python_page(request: Request):
    return render_page(request, "python.html")


@app.get("/java", response_class=HTMLResponse)
async def java_page(request: Request):
    return render_page(request, "java.html")


@app.get("/javascript", response_class=HTMLResponse)
async def javascript_page(request: Request):
    return render_page(request, "javascript.html")


@app.get("/htmlcss", response_class=HTMLResponse)
async def htmlcss_page(request: Request):
    return render_page(request, "htmlcss.html")


@app.get("/php", response_class=HTMLResponse)
async def php_page(request: Request):
    return render_page(request, "php.html")


@app.get("/sql", response_class=HTMLResponse)
async def sql_page(request: Request):
    return render_page(request, "sql.html")


@app.get("/test/{course_name}", response_class=HTMLResponse)
async def show_test(request: Request, course_name: str):
    course = TESTS.get(course_name)

    if not course:
        raise HTTPException(status_code=404, detail="Тест для цього курсу не знайдено")

    return render_page(
        request,
        "test.html",
        course_name=course_name,
        course_title=course["title"],
        questions=course["questions"]
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/profile", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) as total_courses FROM courses")
    total_courses = cursor.fetchone()["total_courses"]

    cursor.execute("SELECT COUNT(*) as total_results FROM test_results")
    total_results = cursor.fetchone()["total_results"]

    cursor.execute("""
        SELECT
            u.id,
            u.username,
            u.email,
            u.role,
            u.created_at,
            COUNT(tr.id) as tests_passed,
            COALESCE(ROUND(AVG((tr.score * 100.0) / tr.total), 1), 0) as avg_result,
            COUNT(DISTINCT tr.course_id) as completed_courses,
            MAX(tr.passed_at) as last_activity
        FROM users u
        LEFT JOIN test_results tr ON u.id = tr.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    """)
    users = cursor.fetchall()

    cursor.execute("""
        SELECT
            u.username,
            u.email,
            c.title as course_title,
            tr.score,
            tr.total,
            tr.passed_at
        FROM test_results tr
        JOIN users u ON tr.user_id = u.id
        JOIN courses c ON tr.course_id = c.id
        ORDER BY tr.passed_at DESC
        LIMIT 12
    """)
    recent_results = cursor.fetchall()

    site_content = get_site_content()

    conn.close()

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
        "total_users": total_users,
        "total_courses": total_courses,
        "total_results": total_results,
        "users": users,
        "recent_results": recent_results,
        "site_content": site_content
    })


@app.post("/admin/update-home")
async def update_home_content(
    request: Request,
    hero_title: str = Form(...),
    hero_subtitle: str = Form(...),

    about_title: str = Form(...),
    about_text_1: str = Form(...),
    about_text_2: str = Form(...),

    audience_title: str = Form(...),
    audience_item_1: str = Form(...),
    audience_item_2: str = Form(...),
    audience_item_3: str = Form(...),
    audience_item_4: str = Form(...),

    features_title: str = Form(...),
    features_item_1: str = Form(...),
    features_item_2: str = Form(...),
    features_item_3: str = Form(...),
    features_item_4: str = Form(...),
    features_item_5: str = Form(...),

    college_title: str = Form(...),
    college_text_1: str = Form(...),
    college_text_2: str = Form(...),

    creator_title: str = Form(...),
    creator_text: str = Form(...),

    skills_title: str = Form(...),
    skills_text_1: str = Form(...),
    skills_text_2: str = Form(...),

    importance_title: str = Form(...),
    importance_text_1: str = Form(...),
    importance_text_2: str = Form(...)
):
    if request.session.get("role") != "admin":
        return JSONResponse({"ok": False, "message": "Доступ лише для адміністратора."})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE site_content
        SET
            hero_title = ?,
            hero_subtitle = ?,

            about_title = ?,
            about_text_1 = ?,
            about_text_2 = ?,

            audience_title = ?,
            audience_item_1 = ?,
            audience_item_2 = ?,
            audience_item_3 = ?,
            audience_item_4 = ?,

            features_title = ?,
            features_item_1 = ?,
            features_item_2 = ?,
            features_item_3 = ?,
            features_item_4 = ?,
            features_item_5 = ?,

            college_title = ?,
            college_text_1 = ?,
            college_text_2 = ?,

            creator_title = ?,
            creator_text = ?,

            skills_title = ?,
            skills_text_1 = ?,
            skills_text_2 = ?,

            importance_title = ?,
            importance_text_1 = ?,
            importance_text_2 = ?
        WHERE id = 1
    """, (
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
    ))

    conn.commit()
    conn.close()

    return JSONResponse({"ok": True, "message": "Головну сторінку успішно оновлено."})

@app.get("/make-admin")
async def make_admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role = 'admin'
        WHERE email = 'vitaliklutchak12@gmail.com'
    """)

    conn.commit()
    conn.close()

    return {"message": "Ти тепер адмін 😎"}

@app.post("/test/{course_name}", response_class=HTMLResponse)
async def submit_test(request: Request, course_name: str):
    course = TESTS.get(course_name)

    if not course:
        raise HTTPException(status_code=404, detail="Тест для цього курсу не знайдено")

    form = await request.form()
    score = 0
    total = len(course["questions"])
    detailed_results = []

    for q in course["questions"]:
        user_answer = form.get(q["id"])
        is_correct = user_answer == q["correct"]

        if is_correct:
            score += 1

        detailed_results.append({
            "question": q["question"],
            "user_answer": user_answer if user_answer else "Не вибрано",
            "correct_answer": q["correct"],
            "is_correct": is_correct
        })

    user_id = request.session.get("user_id")

    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM courses WHERE slug = ?", (course_name,))
        course_row = cursor.fetchone()

        if course_row:
            course_id = course_row["id"]

            cursor.execute("""
                INSERT INTO test_results (user_id, course_id, score, total)
                VALUES (?, ?, ?, ?)
            """, (user_id, course_id, score, total))

            conn.commit()

        conn.close()

    return templates.TemplateResponse("result.html", {
        "request": request,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
        "course_name": course_name,
        "course_title": course["title"],
        "score": score,
        "total": total,
        "details": detailed_results
    })

