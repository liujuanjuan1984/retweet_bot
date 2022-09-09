from retweet_bot import RetweetBot

bot = RetweetBot()


url = "https://example.com/personal_homepage"
name = "somebody"
users = {
    url: {
    "name": name,
    "url": url,
    },
}
bot.retweet_users(users)

