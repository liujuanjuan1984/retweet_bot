"""only for v0.1 to upgrade data from file to db"""

import datetime
import json
import os
import time

from officy import Dir, JsonFile

from retweet_bot import RetweetBot

this_repo = os.path.dirname(__file__)
print(this_repo)
bot = RetweetBot(init=True, skip_driver=True)


def history_user():
    """add history users info into db"""

    v1_user_file = os.path.join(this_repo, "retweet_bot", "users_private.json")
    retweet_status = True
    profile_status = True

    data = JsonFile(v1_user_file).read()
    for user_url in data:
        keystore = json.loads(data[user_url]["keystore"])
        bot.db.update_user(user_url, retweet_status, profile_status, keystore)


def history_post():
    """add history posts info into db"""

    datadir = os.path.join(this_repo, "data")
    userfiles = Dir(datadir).search_files_by_types(".json")
    content_status = None
    retweet_status = True
    for i in userfiles:
        idata = JsonFile(i).read()
        for post_url in idata:
            user_url = "/".join(
                post_url.split("/")[:-1]
            )  # "https://weibo.com/6522911909/Lvzlwb9gp"
            trx_id = idata[post_url].get("trx_id")
            bot.db.update_post_url(
                user_url, post_url, content_status, retweet_status, trx_id
            )
