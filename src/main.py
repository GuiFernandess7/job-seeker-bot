from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

import time
import logging

class JobScraper:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def set_chrome_options(self):
        """Chrome configuration settings"""
        options = Options()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.binary_location = "/usr/bin/google-chrome"

        return options

    def set_webdriver(self, browser="Chrome"):
        options = self.set_chrome_options()
        if browser.lower() == "chrome":
            self.logger.warning("Using Chrome WebDriver.")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        else:
            self.logger.error("Unsupported browser. Only Chrome is supported.")
            raise ValueError("Unsupported browser")

    def __check_driver(self):
        if not self.driver:
            self.logger.error("Driver not initialized.")
            raise RuntimeError("Driver not initialized.")

    def open_url(self, url: str):
        self.__check_driver()
        try:
            self.driver.get(url)
            self.logger.info(f"Opened URL: {url}")
        except Exception as e:
            self.logger.error(f"Failed to open URL: {url} with error: {e}")
            self.driver_quit()

    def apply_search(self, site: str, position: str, mode: str = "remote"):
        self.__check_driver()
        search_phrase = f"site:{site} '{position}''{mode}'"
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys(search_phrase)
        search.send_keys(Keys.RETURN)
        time.sleep(5)

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver quit successfully.")

def run_news_task():
    scraper = JobScraper()
    scraper.set_webdriver()
    scraper.open_url("https://www.google.com")
    scraper.apply_search(site="https://jobs[.]lever[.]co", position="React Developer", mode="remote")
    scraper.driver_quit()

if __name__=="__main__":
    run_news_task()
