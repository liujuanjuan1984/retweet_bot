"""持续运行，通过任务计划程序触发重复"""

import datetime

from retweet_bot import RetweetBot

bot = RetweetBot().spider


print(datetime.datetime.now(), "main task...")
bot.get_profiles()
print(datetime.datetime.now(), "get profiles done")

bot.get_posts()
print(datetime.datetime.now(), "get posts done")

bot.get_new_posturls()
print(datetime.datetime.now(), "get new posturls done")

# bot.get_history_posturls(1, 8)
# print(datetime.datetime.now(),"get history posturls done")

bot.quit()

print(datetime.datetime.now(), "quit")
