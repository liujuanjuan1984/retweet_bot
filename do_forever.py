import datetime
import time

from retweet_bot import RetweetBot

bot = RetweetBot()

while True:
    print(datetime.datetime.now(), "start ...")
    bot.retweet_users()
    time.sleep(5)
