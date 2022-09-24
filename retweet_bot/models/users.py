import logging

from sqlalchemy import Boolean, Column, Integer, String

from retweet_bot.models.base import Base, current_time

logger = logging.getLogger(__name__)


class User(Base):
    """the target users to retweet
    retweet_status:
    None: new user to check
    True: user is valid to retweet
    False: user is invalid to retweet, such as the user is not exist or banned

    profile_status:
    None: profile todo
    True: profile update done
    False: profile update error or failed
    """

    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, unique=True, index=True)
    user_url = Column(String, unique=True, index=True)
    keystore = Column(String)
    retweet_status = Column(Boolean, default=None)
    profile_status = Column(Boolean, default=None)
    created_at = Column(String, default=current_time)
    updated_at = Column(String, default=current_time)

    def __init__(self, obj):
        super().__init__(**obj)
