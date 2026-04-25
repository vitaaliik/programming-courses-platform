from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"

    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""

    session_secret_key: str = "super_secret_key_12345"
    admin_email: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()