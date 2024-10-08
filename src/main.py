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

class JobScraper:

    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def set_chrome_options(self):
        """Chrome configuration settings"""
        options = Options()
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
        """Search for job postings and return results."""
        self.__check_driver()
        search_phrase = f"site:{site} '{position}' '{mode}'"

        wait = WebDriverWait(self.driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(search_phrase)
        search_box.send_keys(Keys.RETURN)

        wait.until(
            EC.presence_of_element_located((By.ID, "search"))
        )

    def __find_search_elements(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "g"))
            )

        except Exception as e:
            print(f"Error waiting for elements: {e}")
            self.driver_quit()

    def __has_application_form(self, url) -> bool:
        self.driver.get(url)

        try:
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            if forms:
                return True

        except Exception as e:
            print(f"Error verifying form: {url} - {e}")

        return False

    @property
    def pages(self):
        pageData = []
        self.__find_search_elements()

        try:
            searchResults = self.driver.find_elements(By.CSS_SELECTOR, "h3.LC20lb")
            urls = []

            for result in searchResults:
                parent = result.find_element(By.XPATH, "..")
                url = parent.get_attribute("href")
                urls.append(url)
                text = result.text
                pageData.append((text, url))

        except Exception as e:
            print(f"Error extracting results: {e}")
            self.driver_quit()

        return pageData

    def apply(self, pageData):
        for _, url in pageData:
            has_form = self.__has_application_form(url)

            if has_form:
                elements = self.driver.find_elements(By.CLASS_NAME, "field")

                for element in elements:
                    try:
                        input_element = element.find_element(By.XPATH, ".//input")
                        print("Input found:", input_element.get_attribute('id'))
                    except NoSuchElementException:
                        logging.info(f"Input not found")
                    else:
                        input_element = element.find_element(By.TAG_NAME, "input")
                        text = element.text
                        if "*" in text:
                            print(f"Field: {text}")
                            print(f"input Name: {input_element.get_attribute('id')}")
                            print('----------')

            break

        return

    def driver_quit(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver quit successfully.")

def run_news_task():
    scraper = JobScraper()
    scraper.set_webdriver()
    scraper.open_url("https://www.google.com")
    # site:https://jobs[.]lever[.]co "React Developer" "remote" -"remote only in the US"
    scraper.apply_search(site="boards[.]greenhouse[.]io", position="Python Developer", mode="remote - remote only in the US")
    results = scraper.pages
    scraper.apply(results)

    for result in results:
        print(result)

    scraper.driver_quit()

if __name__=="__main__":
    run_news_task()
