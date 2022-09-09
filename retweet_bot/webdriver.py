import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


class WebDriver:
    """selenium webdriver"""

    def __init__(self, mode="light"):
        """mode: light, dark"""
        if mode != "light":
            self.driver = self.__start_driver_dark()
        else:
            self.driver = self.__start_driver_light()

    def __start_driver_dark(self):
        """dark mode"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def __start_driver_light(self):
        """light mode"""
        return webdriver.Chrome()
