from sqlalchemy.orm import Session

from src.models.home_block import HomeBlock
from src.models.site_content import SiteContent


class SiteRepository:
    def __init__(self, db: Session):
        self.db = db

    def _site_content_to_dict(self, content: SiteContent) -> dict:
        return {
            "id": content.id,
            "hero_title": content.hero_title,
            "hero_subtitle": content.hero_subtitle,
            "about_title": content.about_title,
            "about_text_1": content.about_text_1,
            "about_text_2": content.about_text_2,
            "audience_title": content.audience_title,
            "audience_item_1": content.audience_item_1,
            "audience_item_2": content.audience_item_2,
            "audience_item_3": content.audience_item_3,
            "audience_item_4": content.audience_item_4,
            "features_title": content.features_title,
            "features_item_1": content.features_item_1,
            "features_item_2": content.features_item_2,
            "features_item_3": content.features_item_3,
            "features_item_4": content.features_item_4,
            "features_item_5": content.features_item_5,
            "college_title": content.college_title,
            "college_text_1": content.college_text_1,
            "college_text_2": content.college_text_2,
            "creator_title": content.creator_title,
            "creator_text": content.creator_text,
            "skills_title": content.skills_title,
            "skills_text_1": content.skills_text_1,
            "skills_text_2": content.skills_text_2,
            "importance_title": content.importance_title,
            "importance_text_1": content.importance_text_1,
            "importance_text_2": content.importance_text_2,
        }

    def _home_block_to_dict(self, block: HomeBlock) -> dict:
        return {
            "id": block.id,
            "title": block.title,
            "content_html": block.content_html,
            "sort_order": block.sort_order,
            "created_at": block.created_at,
        }

    def get_site_content(self) -> dict:
        content = self.db.query(SiteContent).filter(SiteContent.id == 1).first()

        if not content:
            return {}

        return self._site_content_to_dict(content)

    def update_site_hero(self, hero_title: str, hero_subtitle: str) -> None:
        content = self.db.query(SiteContent).filter(SiteContent.id == 1).first()

        if not content:
            return

        content.hero_title = hero_title
        content.hero_subtitle = hero_subtitle

        self.db.flush()

    def get_home_blocks(self) -> list[dict]:
        blocks = (
            self.db.query(HomeBlock)
            .order_by(HomeBlock.sort_order.asc(), HomeBlock.id.asc())
            .all()
        )

        return [self._home_block_to_dict(block) for block in blocks]

    def create_home_block(
        self,
        title: str,
        content_html: str,
        sort_order: int,
    ) -> None:
        block = HomeBlock(
            title=title,
            content_html=content_html,
            sort_order=sort_order,
        )

        self.db.add(block)
        self.db.flush()

    def update_home_block(
        self,
        block_id: int,
        title: str,
        content_html: str,
        sort_order: int,
    ) -> None:
        block = self.db.query(HomeBlock).filter(HomeBlock.id == block_id).first()

        if not block:
            return

        block.title = title
        block.content_html = content_html
        block.sort_order = sort_order

        self.db.flush()

    def delete_home_block(self, block_id: int) -> None:
        self.db.query(HomeBlock).filter(HomeBlock.id == block_id).delete()
        self.db.flush()