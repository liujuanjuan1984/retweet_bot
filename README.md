# retweet_bot

Read the database of SpiderBot and retweet to Quorum Group.

### How to use?

Get the source code:

```sh
git clone https://github.com/liujuanjuan1984/retweet_bot.git
cd retweet_bot 
```

Install:

```sh
pip install -r requirements.txt
```

TIPS: the SpiderBot need chrome browser and [chromedriver](https://chromedriver.chromium.org/downloads).

Update the config_private.py file using config_private_sample.py as example.

Do the main job:

```py
do_spider.py # get content by spiderbot
do_retweet.py # retweet bot to rum by using database of spiderbot as data source
```
