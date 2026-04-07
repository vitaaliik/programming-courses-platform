import smtplib
from email.mime.text import MIMEText

from src.core.config import settings


def send_reset_email(receiver_email: str, code: str) -> None:
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD or not settings.MAIL_FROM:
        raise RuntimeError("Пошта не налаштована. Перевір .env")

    subject = "Код для відновлення пароля"
    body = f"""
Ваш код для відновлення пароля: {code}

Код дійсний 10 хвилин.
Якщо ви не запитували відновлення пароля, просто проігноруйте цей лист.
""".strip()

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM, receiver_email, msg.as_string())