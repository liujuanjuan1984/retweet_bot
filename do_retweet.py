"""持续运行，通过任务计划程序来触发"""
import datetime

from retweet_bot import RetweetBot

bot = RetweetBot(init=True, skip_driver=True)

bot.update_user_from_datadb(profile_status=None)
uid = bot.update_posturl_from_datadb()
print(datetime.datetime.now(), uid)
