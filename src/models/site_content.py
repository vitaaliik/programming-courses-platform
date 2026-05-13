from sqlalchemy import Column, Integer, Text

from src.core.database_sqlalchemy import Base


class SiteContent(Base):
    __tablename__ = "site_content"

    id = Column(Integer, primary_key=True)
    hero_title = Column(Text, nullable=False)
    hero_subtitle = Column(Text, nullable=False)

    about_title = Column(Text, nullable=False)
    about_text_1 = Column(Text, nullable=False)
    about_text_2 = Column(Text, nullable=False)

    audience_title = Column(Text, nullable=False)
    audience_item_1 = Column(Text, nullable=False)
    audience_item_2 = Column(Text, nullable=False)
    audience_item_3 = Column(Text, nullable=False)
    audience_item_4 = Column(Text, nullable=False)

    features_title = Column(Text, nullable=False)
    features_item_1 = Column(Text, nullable=False)
    features_item_2 = Column(Text, nullable=False)
    features_item_3 = Column(Text, nullable=False)
    features_item_4 = Column(Text, nullable=False)
    features_item_5 = Column(Text, nullable=False)

    college_title = Column(Text, nullable=False)
    college_text_1 = Column(Text, nullable=False)
    college_text_2 = Column(Text, nullable=False)

    creator_title = Column(Text, nullable=False)
    creator_text = Column(Text, nullable=False)

    skills_title = Column(Text, nullable=False)
    skills_text_1 = Column(Text, nullable=False)
    skills_text_2 = Column(Text, nullable=False)

    importance_title = Column(Text, nullable=False)
    importance_text_1 = Column(Text, nullable=False)
    importance_text_2 = Column(Text, nullable=False)