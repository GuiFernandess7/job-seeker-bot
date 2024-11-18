from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from abc import ABC, abstractmethod
from typing import List, Tuple

import logging
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class RPABuilder(ABC):

    @abstractmethod
    def get_driver(self) -> webdriver.Chrome:
        pass

class RPAConcreteBuilder(RPABuilder):
    def __init__(self, headless: bool = True, selenium_url: str = None):
        self.headless = headless
        self.selenium_url = selenium_url or os.getenv("SELENIUM_URL", "http://localhost:4444/wd/hub")

    def get_driver(self) -> webdriver.Chrome:
        options = self.__set_chrome_options(headless=self.headless)
        driver = webdriver.Remote(
            command_executor=self.selenium_url,
            options=options
        )
        return driver

    def __set_chrome_options(self, headless: bool = True) -> Options:
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


def is_captcha_present(driver) -> bool:
    try:
        captcha_frame = driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
        return captcha_frame.is_displayed()
    except Exception:
        return False

class RPABot:
    def __init__(self, driver, initial_url: str = "https://www.google.com") -> None:
        self.driver = driver
        self.initial_url = initial_url

    def get_search_box(self, element_name: str = "q", time_to_wait: int = 20):
        self.driver.get(self.initial_url)
        logging.info(f"Opened URL: {self.initial_url}")

        try:
            search_box = WebDriverWait(self.driver, time_to_wait).until(
                EC.presence_of_element_located((By.NAME, element_name))
            )
        except TimeoutException:
            logging.error("Timeout: Não foi possível localizar a caixa de pesquisa.")
            return None

        return search_box

    def apply_search(self, query: str) -> None:
        search_box = self.get_search_box()
        if search_box is None:
            return

        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
        except TimeoutException:
            logging.error("Timeout: Não foi possível localizar os resultados da pesquisa.")
            return

        logging.info(f"Search applied with query: {query}")

    def check_for_captcha(self, query: str) -> bool:
        if is_captcha_present(self.driver):
            logging.warning(f"Skipping extraction for query '{query}' due to CAPTCHA.")
            return True
        return False

    def get_results(self, query: str, link_element: str = "h3.LC20lb") -> List[Tuple[str, str]]:
        search_results = []
        try:
            results = self.driver.find_elements(By.CSS_SELECTOR, link_element)
            for result in results:
                url = result.find_element(By.XPATH, "..").get_attribute("href")
                search_results.append((result.text, url))
            logging.info(f"Extracted {len(results)} results for query '{query}'.")
        except Exception as e:
            logging.error(f"Error extracting results for query '{query}': {e}")

        return search_results

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            logging.info("Driver closed.")

class JobSeekerBot:
    def __init__(self, driver: webdriver.Chrome):
        self.bot = RPABot(driver)

    def search_and_extract(self, queries: List[str]) -> None:
        for query in queries:
            self.bot.apply_search(query)

            if self.bot.check_for_captcha(query):
                continue

            results = self.bot.get_results(query)
            if results:
                for result in results:
                    logging.info(f"Title: {result[0]}, URL: {result[1]}")
            else:
                logging.warning(f"No results found for query '{query}'")

def main():
    builder = RPAConcreteBuilder(headless=True, selenium_url="http://selenium:4444/wd/hub")
    driver = builder.get_driver()
    bot = JobSeekerBot(driver)

    queries = [
        "site:netvagas.com.br python junior developer",
        "site:boards.greenhouse.io python junior developer",
        "site:infojobs.com.br python junior developer remoto",
        "site:catho.com.br python junior developer remoto",
        "site:linkedin.com/jobs python junior developer remoto",
        "site:glassdoor.com.br python junior developer remoto",
        "site:indeed.com.br python junior developer remoto",
    ]

    bot.search_and_extract(queries)

main()

""" all_results = {}
for query in queries:
    results = bot.apply_search_and_extract(query)
    all_results[query] = results

bot.close_driver()

for query, result in all_results.items():
    logging.info(f"Results for query '{query}': {result}") """

""" logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_captcha_present(driver):
    try:
        captcha_frame = driver.find_element(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
        if captcha_frame:
            logging.warning("Captcha detected on the page.")
            return True
    except Exception:
        return False
    return False

def set_chrome_options(headless=True):
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

def start_driver():
    selenium_url = "http://selenium:4444/wd/hub"
    options = set_chrome_options(headless=True)
    driver = webdriver.Remote(
        command_executor=selenium_url,
        options=options
    )
    return driver

def apply_search_and_extract(driver, query):
    driver.get("https://www.google.com")
    logging.info(f"Opened URL: https://www.google.com")

    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    logging.info(f"Search applied with query: {query}")

    if is_captcha_present(driver):
        logging.warning(f"Skipping extraction for query '{query}' due to CAPTCHA.")
        return []

    search_results = []
    try:
        results = driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb")
        for result in results:
            url = result.find_element(By.XPATH, "..").get_attribute("href")
            search_results.append((result.text, url))
        logging.info(f"Extracted {len(results)} results for query '{query}'.")
    except Exception as e:
        logging.error(f"Error extracting results for query '{query}': {e}")

    return search_results

queries = [
        "site:netvagas.com.br python junior developer",
        "site:boards.greenhouse.io python junior developer",
        "site:infojobs.com.br python junior developer remoto",
        "site:catho.com.br python junior developer remoto",
        "site:linkedin.com/jobs python junior developer remoto",
        "site:glassdoor.com.br python junior developer remoto",
        "site:indeed.com.br python junior developer remoto",
    ]

driver = start_driver()

all_results = {}
for query in queries:
    results = apply_search_and_extract(driver, query)
    all_results[query] = results

driver.quit()

for query, result in all_results.items():
    logging.info(f"Results for query '{query}': {result}")
 """