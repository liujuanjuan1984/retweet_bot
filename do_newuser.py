from retweet_bot import RetweetBot

bot = RetweetBot()


url = "https://example.com/personal_homepage"
name = "somebody"
bot.retweet_user(name, url)
