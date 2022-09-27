"""add new users to the spiderbot db"""

import datetime
import time

from retweet_bot import RetweetBot

data = """
https://example.com/1234567
https://example.com/1234568
"""

users = [i for i in data.split("\n") if len(i) > 5]
print(users)

bot = RetweetBot(init=True, skip_driver=True)
bot.spider.add_users(True, *users)
