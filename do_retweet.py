import datetime
import time

from retweet_bot import RetweetBot

bot = RetweetBot(init=True)


uid = 1
while True:
    bot.update_user_from_datadb(profile_status=None)
    uid = bot.update_posturl_from_datadb(uid)
    print(datetime.datetime.now(), uid)
    time.sleep(5)
