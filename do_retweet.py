import datetime
import sys
import time

from retweet_bot import RetweetBot

print(datetime.datetime.now(), "do_retweet start ...")

bot = RetweetBot(init=True)

try:
    print(datetime.datetime.now(), "get_history_posturls start ...")
    bot.spider.get_history_posturls(1, 8)
except KeyboardInterrupt:
    print(datetime.datetime.now(), "KeyboardInterrupt Exiting get_history_posturls ...")
    pass

print(datetime.datetime.now(), "get_history_posturls end")


while True:

    try:
        print(datetime.datetime.now(), "while loop start ...")
        bot.spider.get_profiles()
        bot.spider.get_posts()
        bot.update_user_from_datadb(profile_status=None)
        uid = bot.update_posturl_from_datadb()
        bot.spider.get_new_posturls()
        time.sleep(1)
    except KeyboardInterrupt:
        print(datetime.datetime.now(), "KeyboardInterrupt Exiting while loop ...")
        bot.spider.quit()
        sys.exit(0)
        break
