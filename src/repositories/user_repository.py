from src.core.database import get_db_connection


def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user


def create_user(username: str, email: str, password_hash: str, role: str = "user"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (username, email, password_hash, role),
    )

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id

def create_password_reset(email: str, code: str, expires_at: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM password_resets WHERE email = ?", (email,))
    cursor.execute(
        """
        INSERT INTO password_resets (email, reset_code, expires_at)
        VALUES (?, ?, ?)
        """,
        (email, code, expires_at),
    )

    conn.commit()
    conn.close()


def get_password_reset(email: str, code: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM password_resets
        WHERE email = ? AND reset_code = ?
        ORDER BY id DESC LIMIT 1
        """,
        (email, code),
    )
    reset_row = cursor.fetchone()

    conn.close()
    return reset_row


def delete_password_resets(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM password_resets WHERE email = ?", (email,))

    conn.commit()
    conn.close()


def update_user_password(email: str, password_hash: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE email = ?
        """,
        (password_hash, email),
    )

    conn.commit()
    conn.close()