from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import DatabaseException, NotFoundException, ValidationException
from src.repositories.site_repository import SiteRepository


class SiteService:
    def __init__(self, repository: SiteRepository):
        self.repository = repository

    def get_site_content(self):
        return self.repository.get_site_content()

    def get_home_blocks(self):
        return self.repository.get_home_blocks()

    def update_home_hero(self, data: dict):
        hero_title = data["hero_title"].strip()
        hero_subtitle = data["hero_subtitle"].strip()

        if not hero_title or not hero_subtitle:
            raise ValidationException("Заголовок і підзаголовок не можуть бути порожніми.")

        try:
            self.repository.update_site_hero(hero_title, hero_subtitle)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити hero-блок") from exc

    def get_home_editor_data(self):
        return {
            "site_content": self.repository.get_site_content(),
            "home_blocks": self.repository.get_home_blocks(),
        }

    def add_new_home_block(self, title: str, content_html: str, sort_order: int):
        title = title.strip()
        content_html = content_html.strip()

        if not title:
            raise ValidationException("Назва блоку не може бути порожньою.")

        try:
            self.repository.create_home_block(title, content_html, sort_order)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося додати блок головної сторінки") from exc

    def save_home_block(self, block_id: int, title: str, content_html: str, sort_order: int):
        title = title.strip()
        content_html = content_html.strip()

        if not title:
            raise ValidationException("Назва блоку не може бути порожньою.")

        try:
            self.repository.update_home_block(block_id, title, content_html, sort_order)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося оновити блок головної сторінки") from exc

    def remove_home_block(self, block_id: int):
        try:
            self.repository.delete_home_block(block_id)
            self.repository.db.commit()
            return True

        except SQLAlchemyError as exc:
            self.repository.db.rollback()
            raise DatabaseException("Не вдалося видалити блок головної сторінки") from exc