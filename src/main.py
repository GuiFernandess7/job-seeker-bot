from __future__ import annotations
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

import logging

class RPAProduct:
    def __init__(self):
        self.driver = None
        self.search_results = []

    def set_search_results(self, results):
        self.search_results = results

    def get_search_results(self):
        return self.search_results

class RPABuilder(ABC):
    @property
    @abstractmethod
    def product(self) -> RPAProduct:
        pass

    @abstractmethod
    def set_driver(self, browser: str) -> RPABuilder:
        pass

    @abstractmethod
    def set_chrome_options(self) -> None:
        pass

    @abstractmethod
    def open_url(self, url: str) -> RPABuilder:
        pass

    @abstractmethod
    def find_search_elements(self) -> RPABuilder:
        pass

    @abstractmethod
    def apply_search(self, query: str) -> RPABuilder:
        pass

    @abstractmethod
    def extract_websites(self) -> RPABuilder:
        pass

    @abstractmethod
    def driver_quit(self) -> None:
        pass

class RPAConcreteBuilder(RPABuilder):
    def __init__(self):
        self._driver = RPAProduct()

    @property
    def product(self) -> RPAProduct:
        product = self._driver
        self.reset()
        return product

    def reset(self) -> None:
        self._driver = RPAProduct()

    def set_driver(self, browser: str = "Chrome") -> RPABuilder:
        options = self.set_chrome_options()
        if browser.lower() == "chrome":
            self._driver.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        else:
            raise ValueError("Unsupported browser")
        return self

    def set_chrome_options(self, headless: bool = False) -> None:
        options = Options()
        if headless:
            options.add_argument("--headless")

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

    def open_url(self, url: str) -> RPABuilder:
        self._driver.driver.get(url)
        return self

    def find_search_elements(self) -> RPABuilder:
        self._driver.driver.find_element(By.NAME, "q")
        return self

    def apply_search(self, query: str) -> RPABuilder:
        search_box = self._driver.driver.find_element(By.NAME, "q")
        wait = WebDriverWait(self._driver.driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        wait.until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        return self

    def extract_websites(self) -> RPABuilder:
        searchResults = self._driver.driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb")

        try:
            for result in searchResults:
                parent = result.find_element(By.XPATH, "..")
                url = parent.get_attribute("href")
                text = result.text
                self._driver.search_results.append((text, url))

        except Exception as e:
            print(f"Error extracting results: {e}")
            self.driver_quit()
        return self

    def driver_quit(self) -> None:
        if self._driver.driver:
            self._driver.driver.quit()

class JobSeekerBot:

    def __init__(self, builder: RPABuilder) -> None:
        self._builder = builder

    @property
    def builder(self) -> RPABuilder:
        return self._builder

    def build_minimal_viable_product(self, url: str) -> None:
        self.builder.set_driver().open_url(url)

    def build_full_featured_product(self, url: str, search_query: str) -> None:
        self.builder.set_driver()\
            .open_url(url)\
            .find_search_elements()\
            .apply_search(search_query)\
            .extract_websites()

def configure_logging():
    logging.basicConfig(level=logging.INFO)

if __name__=="__main__":
    configure_logging()
    builder = RPAConcreteBuilder()
    bot = JobSeekerBot(builder)

    search_phrase = "React Developer" "remote" " - remote only in the US"
    bot.build_full_featured_product('http://www.google.com', search_phrase)
    search_results = builder.product.get_search_results()

    for result in search_results:
        print(result)

    builder.driver_quit()
