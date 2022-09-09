import datetime
import logging

from retweet_bot.bot import RetweetBot
from retweet_bot.config_private import SEED, XPATHS
from retweet_bot.jsonfile import JsonFile

__version__ = "0.1.0"
__author__ = "liujuanjuan1984"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename=f"retweet_{datetime.date.today()}.log",
    level=logging.INFO,
)
