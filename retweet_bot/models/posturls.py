import logging

from sqlalchemy import Boolean, Column, Integer, String

from retweet_bot.models.base import Base, current_time

logger = logging.getLogger(__name__)


class PostURL(Base):
    """the url of the posts
    status:
    None: todo
    True: done
    False: error or failed
    """

    __tablename__ = "post_urls"

    uid = Column(Integer, primary_key=True, unique=True, index=True)
    user_url = Column(String, index=True)
    post_url = Column(String, unique=True, index=True)
    content_status = Column(Boolean, default=None)
    retweet_status = Column(Boolean, default=None)
    trx_id = Column(String, default=None)
    on_chain = Column(Boolean, default=None)
    created_at = Column(String, default=current_time)
    updated_at = Column(String, default=current_time)

    def __init__(self, obj):
        super().__init__(**obj)
