"""api.py"""
import json
import logging
from typing import Dict, Optional

from eth_account import Account

from retweet_bot.config_private import COMMON_ACCOUNT_PWD
from retweet_bot.models.base import BaseDB
from retweet_bot.models.posturls import PostURL
from retweet_bot.models.users import User

logger = logging.getLogger(__name__)


class DBAPI(BaseDB):
    def update_user(
        self,
        user_url,
        retweet_status: Optional[bool] = None,
        profile_status: Optional[bool] = None,
        keystore: Optional[Dict] = None,
    ):
        """add/update user to db"""
        user = self.session.query(User).filter(User.user_url == user_url).first()
        if not user:
            if keystore is None:
                account = Account().create()
                keystore = account.encrypt(COMMON_ACCOUNT_PWD)
            self.add(
                User(
                    {
                        "user_url": user_url,
                        "retweet_status": retweet_status,
                        "profile_status": profile_status,
                        "keystore": json.dumps(keystore),
                    }
                )
            )
            logger.info("add user %s", user_url)
        else:
            _params = {}
            if retweet_status is not None:
                _params["retweet_status"] = retweet_status
            if profile_status is not None:
                _params["profile_status"] = profile_status
            if keystore is not None:
                _params["keystore"] = json.dumps(keystore)
            if _params:
                self.session.query(User).filter(User.user_url == user_url).update(
                    _params
                )
                self.commit()
                logger.info("update user %s", user_url)

    def get_pvtkey(self, keystore):
        """get private key"""
        if isinstance(keystore, str):
            keystore = json.loads(keystore)
        pvtkey = Account().decrypt(keystore, COMMON_ACCOUNT_PWD)
        return pvtkey

    def get_pvtkeys(self):
        """get all private keys"""
        users = self.session.query(User).all()
        keys = {}
        for user in users:
            if user.keystore:
                keys[user.user_url] = self.get_pvtkey(user.keystore)
        return keys

    def get_user_pvtkey(self, user_url):
        """get user private key by url"""
        user = self.session.query(User).filter(User.user_url == user_url).first()
        if user:
            keystore = user.keystore
        else:
            logger.info("get_user_pvtkey but user not existd %s", user_url)
            return None
        return self.get_pvtkey(keystore)

    def update_user_profile_status(self, user_url: str, profile_status: bool):
        """update status of profile"""
        self.session.query(User).filter(User.user_url == user_url).update(
            {"profile_status": profile_status}
        )
        self.commit()

        logger.info("update_user_profile_status %s", user_url)

    def update_user_retweet_status(self, user_url: str, retweet_status: bool):
        """update status of working"""
        self.session.query(User).filter(User.user_url == user_url).update(
            {"retweet_status": retweet_status}
        )
        self.commit()
        logger.info("update_user_retweet_status %s", user_url)

    def update_post_url(
        self,
        user_url: str,
        post_url: str,
        content_status: Optional[bool] = None,
        retweet_status: Optional[bool] = None,
        trx_id: Optional[str] = None,
        on_chain: Optional[bool] = None,
    ):
        """add or update post url to db"""
        url = self.session.query(PostURL).filter(PostURL.post_url == post_url).first()
        # if not exist, add it
        if not url:
            self.add(
                PostURL(
                    {
                        "user_url": user_url,
                        "post_url": post_url,
                        "content_status": content_status,
                        "retweet_status": retweet_status,
                        "trx_id": trx_id,
                        "on_chain": on_chain,
                    }
                )
            )
            logger.info("add post url %s", post_url)
        else:
            _params = {}
            if content_status is not None:
                _params["content_status"] = content_status
            if retweet_status is not None:
                _params["retweet_status"] = retweet_status
            if trx_id is not None:
                _params["trx_id"] = trx_id
            if on_chain is not None:
                _params["on_chain"] = on_chain

            if _params:
                self.session.query(PostURL).filter(PostURL.post_url == post_url).update(
                    _params
                )
                self.commit()
                logger.info("update_post_url %s", post_url)

    def check_posturl_to_retweet(self, post_url: str) -> bool:
        """check the post url to retweet"""
        need_retweet = True
        post_url = (
            self.session.query(PostURL).filter(PostURL.post_url == post_url).first()
        )

        if post_url:
            if post_url.retweet_status:
                need_retweet = False
        logger.info("check_posturl_to_retweet %s %s", need_retweet, post_url)
        return need_retweet

    def check_profile_to_retweet(self, user_url: str, profile_status) -> bool:
        """check the profile to retweet"""
        need_retweet = False
        user = (
            self.session.query(User)
            .filter(User.user_url == user_url)
            .filter(User.profile_status == profile_status)
            .first()
        )
        if user:
            need_retweet = True
        logger.info("check_profile_to_retweet %s %s", need_retweet, user_url)
        return need_retweet
