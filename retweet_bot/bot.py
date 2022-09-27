"""bot.py"""

import logging

from mininode import MiniNode
from spiderbot import SpiderBot

from retweet_bot.config_private import *  # COMMON_ACCOUNT_PWD, DATA_DB_NAME, DB_NAME,SEED ,
from retweet_bot.models.api import DBAPI as RetweetAPI

logger = logging.getLogger(__name__)


class RetweetBot:
    """retweet bot"""

    def __init__(
        self,
        seedurl: str = None,
        data_db_name=None,
        db_name=None,
        skip_driver=False,
        xpaths=None,
        init=None,
        **kwargs,
    ):
        """data_db_name:the db_name of spiderbot"""
        self.rum = MiniNode(seedurl or SEED)
        self.db = RetweetAPI(db_name or DB_NAME, init=init, **kwargs)
        self.spider = SpiderBot(
            data_db_name or DATA_DB_NAME,
            skip_driver=skip_driver,
            xpaths=xpaths or XPATHS,
            init=init,
        )
        self.keys = self.db.get_pvtkeys()

    def update_user_from_datadb(
        self, retweet_status=True, profile_status=None, keystore=None
    ):
        """add or update user from data database to retweet database"""
        for user in self.spider.db.get_users_todo(working_status=True):
            user_url = user[0]
            self.db.update_user(user_url, retweet_status, profile_status, keystore)

    def update_posturl_from_datadb(self, uid=None):
        """add or update posturl from data database to retweet database"""
        uid = uid or self.db.get_progress("update_posturl_from_datadb")
        logger.info("update_posturl_from_datadb: %s", uid)
        posts = self.spider.db.get_posts(uid=uid)
        for post in posts:
            uid = post.uid
            logger.info("update posturl: %s %s", uid, post.post_url)
            post_url = post.post_url
            user_url = "/".join(post_url.split("/")[:-1])
            retweet_status = None
            need_retweet = self.db.check_posturl_to_retweet(post_url)
            pvtkey = self.keys.get(user_url)
            if not pvtkey:
                logger.warning("no pvtkey: %s", user_url)
                continue
            trx_id = None
            if need_retweet:
                resp = self.send_post_to_rum(pvtkey, post)
                trx_id = resp.get("trx_id")
                retweet_status = "trx_id" in resp

            if post.text or post.screenshot:
                content_status = True
            else:
                content_status = False
            self.db.update_post_url(
                user_url, post_url, content_status, retweet_status, trx_id
            )
            self.db.update_progress("update_posturl_from_datadb", uid)
        return uid

    def send_post_to_rum(self, pvtkey, post):
        """send posts to rum group"""
        text = post.text
        img = post.screenshot
        if text or img:
            text = (text or "") + f"""\n{TIPS[LANG]['origin']}: {post.post_url}"""
            resp = self.rum.api.send_content(
                pvtkey, content=text, images=[img], timestamp=post.post_time
            )
            return resp

    def send_profiles_to_rum(self, profile_status=None, uid=1):
        """update user profile in rum group
        profile_status:None,True,False
        """
        for user in self.spider.db.get_profiles(uid):
            user_url = user.user_url
            need_profile = self.db.check_profile_to_retweet(user_url, profile_status)
            if not need_profile:
                continue
            pvtkey = self.keys.get(user_url)
            if pvtkey and user.name and user.avatar:
                name = f"{user.name}@{TIPS[LANG]['name']}"
                resp = self.rum.api.update_profile(pvtkey, name=name, image=user.avatar)
                if "trx_id" in resp:
                    logger.info("update profile: %s %s", user.user_url, name)
                    self.db.update_user_profile_status(user_url, True)
                else:
                    logger.warning("update profile failed: %s %s ", user.user_url, name)
