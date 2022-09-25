import logging

from sqlalchemy import Column, Integer, String

from retweet_bot.models.base import Base, current_time

logger = logging.getLogger(__name__)


class Progress(Base):
    """the uid of progress"""

    __tablename__ = "progress"

    uid = Column(Integer, primary_key=True, unique=True)
    progress_type = Column(String, unique=True)
    progress_uid = Column(Integer)
    created_at = Column(String, default=current_time)
    updated_at = Column(String, default=current_time)

    def __init__(self, obj):
        super().__init__(**obj)
