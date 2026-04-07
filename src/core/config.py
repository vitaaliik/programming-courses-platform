import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_NAME = "database.db"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM = os.getenv("MAIL_FROM", "")

    SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "super_secret_key_12345")


settings = Settings()