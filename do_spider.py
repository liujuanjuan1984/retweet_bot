import datetime
import time

from retweet_bot import RetweetBot

bot = RetweetBot().spider


while True:
    bot.get_profiles()
    bot.get_new_posturls()
    bot.get_posts()
    bot.get_history_posturls(1, 8)
    print(datetime.datetime.now(), "sleep 10s")
    time.sleep(10)

bot.quit()
