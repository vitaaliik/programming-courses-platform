from sqlalchemy.exc import SQLAlchemyError

from src.repositories.site_repository_sqlalchemy import SiteRepository


class SiteService:
    def __init__(self, repository: SiteRepository):
        self.repository = repository

    def get_site_content(self):
        return self.repository.get_site_content()

    def get_home_blocks(self):
        return self.repository.get_home_blocks()

    def update_home_hero(self, data: dict):
        try:
            self.repository.update_site_hero(
                hero_title=data["hero_title"].strip(),
                hero_subtitle=data["hero_subtitle"].strip(),
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def get_home_editor_data(self):
        return {
            "site_content": self.repository.get_site_content(),
            "home_blocks": self.repository.get_home_blocks(),
        }

    def add_new_home_block(self, title: str, content_html: str, sort_order: int):
        if not title.strip():
            return False

        try:
            self.repository.create_home_block(
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def save_home_block(self, block_id: int, title: str, content_html: str, sort_order: int):
        if not title.strip():
            return False

        try:
            self.repository.update_home_block(
                block_id=block_id,
                title=title.strip(),
                content_html=content_html.strip(),
                sort_order=sort_order,
            )
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False

    def remove_home_block(self, block_id: int):
        try:
            self.repository.delete_home_block(block_id)
            self.repository.db.commit()
            return True
        except SQLAlchemyError:
            self.repository.db.rollback()
            return False