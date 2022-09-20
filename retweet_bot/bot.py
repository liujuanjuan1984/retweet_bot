import base64
import datetime
import json
import logging
import os
from typing import Dict, Optional

from mininode import MiniNode
from mininode.crypto import account
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from retweet_bot.config_private import *
from retweet_bot.jsonfile import JsonFile
from retweet_bot.webdriver import WebDriver

logger = logging.getLogger(__name__)

thisdir = os.path.dirname(__file__)
datadir = os.path.join(os.path.dirname(thisdir), "data")


class RetweetBot:
    """retweet bot"""

    def __init__(self, seedurl: str = None, xpaths: Dict[str, str] = None, mode="dark"):
        self.driver = WebDriver(mode).driver
        self.rum = MiniNode(seedurl or SEED)
        self.xpaths = xpaths or XPATHS
        self.users_file = os.path.join(thisdir, "users_private.json")

    def update_user_profile(self, name, url):
        """update user profile in rum group with the avatar in user homepage url"""
        # get avatar
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 10)
            _element = wait.until(
                EC.presence_of_element_located((By.XPATH, self.xpaths["avatar"]))
            )
        except Exception as err:
            logger.warning("get avatar failed: %s", url)
            return
        avatar = base64.b64decode(_element.screenshot_as_base64)
        name = f"{name}@{TIPS[LANG]['name']}"
        # post to rum group
        pvtkey = self.get_user_pvtkey(name, url)
        resp = self.rum.api.update_profile(pvtkey, name=name, image=avatar)
        if "trx_id" in resp:
            logger.info("update profile: %s", url)
        else:
            logger.warning("update profile failed: %s", url)

    def check_profiles(self, users: Optional[Dict] = None):
        """check users profile and updated if needed"""
        users = users or JsonFile(self.users_file).read({})
        for url in users:
            name = users[url]["name"]
            pvtkey = self.get_user_pvtkey(name, url)
            pubkey = account.private_key_to_pubkey(pvtkey)
            user = self.rum.api.get_profiles(types=("name", "image"), senders=[pubkey])
            # check the profile and update if needed
            existed = user.get(pubkey, {}).get("image")
            if not existed:
                self.update_user_profile(name, url)

    def retweet_users(self, users: Optional[Dict] = None):
        """retweet users
        users = {
            "https://example.com/personal_homepage": {
            "name": "somebody",
            "url": "https://example.com/personal_homepage",
            },
        }

        """
        users = users or JsonFile(self.users_file).read({})
        for url in users:
            name = users[url]["name"]
            try:
                self.retweet_user(name, url)
            except:
                logger.warning("retweet user failed: %s", name + url)

    def retweet_user(self, name: str, url: str):
        """retweet one user"""

        logger.debug("retweet user: %s", name)
        pvtkey = self.get_user_pvtkey(name, url)

        # create/read users datafile, update profile if new user
        user_id = url.split("/")[-1]
        datafile = os.path.join(datadir, f"{user_id}_{name}.json")
        if not os.path.exists(datafile):
            self.update_user_profile(name, url)
            JsonFile(datafile).write({})
        data = JsonFile(datafile).read({})

        # get new posts
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        _elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, self.xpaths["posts"]))
        )

        for _ele in _elements:
            _url = _ele.get_attribute("href")
            if _url.startswith(url) and _url not in data:
                data[_url] = {"created_at": str(datetime.datetime.now())}
                logger.debug("new post: %s", _url)

        for _url in data:
            if "updated_at" in data[_url]:
                continue

            self.driver.get(_url)
            wait = WebDriverWait(self.driver, 10)
            _ele = wait.until(
                EC.presence_of_element_located((By.XPATH, self.xpaths["screenshot"]))
            )
            # screenshot of post
            try:
                img = base64.b64decode(_ele.screenshot_as_base64)
            except Exception as err:
                print(err)
                img = None

            # date
            date_str = (
                "20" + self.driver.find_element(By.XPATH, self.xpaths["date"]).text
            )

            # text content
            try:
                text = self.driver.find_element(By.XPATH, self.xpaths["text"]).text
            except Exception as err:
                logger.warning(err)
                text = None

            # retweet
            if text or img:
                if ORIGIN_URL_TYPE == "MERGE":
                    text += f""" <a href="{_url}" class="text-blue-400">{TIPS[LANG]['origin']}</a>"""
                resp = self.rum.api.send_content(
                    pvtkey, content=text, images=[img], timestamp=date_str
                )

                if "trx_id" not in resp:
                    logger.warning("retweet failed: %s", resp)
                    continue

                data[_url]["updated_at"] = str(datetime.datetime.now())
                data[_url]["trx_id"] = resp["trx_id"]

                if ORIGIN_URL_TYPE == "SPLIT":
                    # reply with the origin url
                    resp_reply = self.rum.api.reply_trx(
                        pvtkey,
                        resp["trx_id"],
                        content=f"{TIPS[LANG]['origin']}{_url}",
                        timestamp=date_str,
                    )
                    if "trx_id" in resp_reply:
                        data[_url]["reply_origin"] = resp_reply["trx_id"]
                    else:
                        logger.warning("reply failed: %s", resp_reply)

                JsonFile(datafile).write(data)
                logger.debug("retweet: %s", resp["trx_id"])

    def get_user_pvtkey(self, name: str, url: str) -> str:
        users = JsonFile(self.users_file).read({})
        user_info = users.get(url, {})
        if "keystore" not in user_info:
            user_info = self.new_user(name, url)
            users[url] = user_info
            JsonFile(self.users_file).write(users)
            logger.info("init new user %s", name)
        keystore = json.loads(user_info["keystore"])
        pvtkey = account.keystore_to_private_key(keystore, USER_ACCOUNT_PASSWORD)
        return pvtkey

    def new_user(self, name: str, url: str, pvtkey: str = None) -> Dict[str, str]:
        pvtkey = pvtkey or account.create_private_key()
        keystore = account.private_key_to_keystore(pvtkey, USER_ACCOUNT_PASSWORD)
        user_info = {
            "name": name,
            "url": url,
            "keystore": json.dumps(keystore),
        }
        return user_info
