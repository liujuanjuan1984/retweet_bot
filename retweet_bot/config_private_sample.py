"""the private config file for the retweet bot; never git push it to github"""

# please update this file with fake data as example.

import os

DB_NAME = f"sqlite:///{os.path.dirname(os.path.dirname(__file__))}/retweet_bot.db"


# the xpath for one post page
XPATHS = {
    "date": r'//*[@id="app"]/div[1]/article/div[2]/header/div[1]/div/div[2]/a',
    "text": r'//*[@id="app"]/div[1]/article/div[2]/div[1]/div[1]/div',
    "screenshot": r'//*[@id="app"]/div[1]/article/div[2]',
    "posts": r'//a[starts-with(@href,"https://example.com/")]',
    "name": r'//*[@id="app"]/div[1]/main/div[1]/div',
    "avatar": r'//*[@id="app"]/div[1]/main/div/div[2]/',
    "history": r'//*[@id="__sidebar"]//div//button',
}


# the seedurl of rum group to send the post
SEED = "rum://seed?v=1&e=0&n=0&b=V5UY8hl0QDiKJz7KX8N-XA&c=4B9LjtcDNhKKG-3RqrSFTUYfzpHIjv9mT1emY6xToF0&g=gMsgqnJMQcWZwUAO3MHuRQ&k=Am-CzxcN1tCKnPO_VmOYQFkWnGjhxZmf0jvCBSTDTXUy&s=6b76vCc38lDxpK2SA6Gepr9takMT_ylmLvVtNMoziW9S9yihwA8SBe4IDBHLSgLeSHePx4dQcyD9YVK2U7Z3ogA&t=FxLw-gXgCOg&a=121&y=group_timeline&u=http%3A%2F%2F127.0.0.1%3A57772%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyI4MGNiMjBhYS03MjRjLTQxYzUtOTljMS00MDBlZGNjMWVlNDUiXSwiZXhwIjoxODIwMzM2MTY5LCJuYW1lIjoiYWxsb3ctODBjYjIwYWEtNzI0Yy00MWM1LTk5YzEtNDAwZWRjYzFlZTQ1Iiwicm9sZSI6Im5vZGUifQ.J2VjP90YgkXCo_MG641QMZR5AHZ7tMCrTrFQ4HooYjY"

# the password of users to get keystore from private_key or private_key to keystore
COMMON_ACCOUNT_PWD = "your-password-keep-it-sercet"


LANG = "CN"

TIPS = {
    "CN": {
        "name": "机器人",
        "origin": "查看全文",
    },
    "EN": {
        "name": "bot",
        "origin": "origin url",
    },
}
