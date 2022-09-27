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
        print(user_url)
        bot.db.update_user(user_url, retweet_status, profile_status, keystore)
        bot.spider.db.add_user(user_url, True)


def history_post():
    """add history posts info into db"""

    datadir = os.path.join(this_repo, "data")
    userfiles = Dir(datadir).search_files_by_types(".json")
    content_status = None
    retweet_status = True
    for i in userfiles:
        idata = JsonFile(i).read()
        for post_url in idata:
            user_url = "/".join(post_url.split("/")[:-1])
            trx_id = idata[post_url].get("trx_id")
            bot.db.update_post_url(
                user_url, post_url, content_status, retweet_status, trx_id
            )
            bot.spider.db.add_post_url(user_url, post_url)


def update_data_from_retweetdb():

    from retweet_bot.models import PostURL, User

    users = (
        bot.db.session.query(User.user_url).filter(User.retweet_status != False).all()
    )
    for i in users:
        bot.spider.db.add_user(i[0], True)

    posts = bot.db.session.query(PostURL).all()
    for i in posts:
        bot.spider.db.add_post_url(i.user_url, i.post_url)


if __name__ == "__main__":
    # history_user()
    # history_post()
    update_data_from_retweetdb()
