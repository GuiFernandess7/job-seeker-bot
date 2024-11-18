import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from src.services.rpa.bot import RPAConcreteBuilder, JobSeekerBot
from src.services.job_post.db.config import DBConnectionHandler

import os

def write_results(path: str, mode: str = "w", result=None):
    row = str(result) + '\n'
    with open(path, mode) as f:
        logging.info(F'[DATA] - {row}')
        f.write(row)

if __name__ == "__main__":
    job_queries = [
        "site:netvagas.com.br python junior developer",
        "site:boards.greenhouse.io python junior developer"
        #"site:infojobs.com.br python junior",
        #"site:catho.com.br python junior",
        #"site:linkedin.com/jobs python junior",
        #"site:glassdoor.com.br python junior",
        #"site:indeed.com.br python junior",
    ]

    all_results = []
    DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
    dest_folder = './data'
    full_path = os.path.join(dest_folder, 'results.txt')

    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        logging.info(f"Directory {dest_folder} created.")

    builder = RPAConcreteBuilder()
    bot = JobSeekerBot(builder)

    try:
        logging.info(f"Initializing search for: {job_queries[0]}")
        bot.build_full_featured_product('http://www.google.com', job_queries[0])

        search_results = builder.product.get_search_results()

        if search_results:
            all_results.extend(search_results)
            logging.info(f"Results saved.")
        else:
            logging.warning(f"Nothing found for query: {job_queries[0]}")

        builder.reset()
        logging.info("Search completed. All results have been saved to the file.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        builder.reset()

    builder = RPAConcreteBuilder()
    bot = JobSeekerBot(builder)

    logging.info(f"Initializing search for: {job_queries[1]}")
    bot.build_full_featured_product('http://www.google.com', job_queries[1])

    search_results = builder.product.get_search_results()

    if search_results:
        all_results.extend(search_results)
        logging.info(f"Results saved.")
    else:
        logging.warning(f"Nothing found for query: {job_queries[1]}")

    for result in all_results:
        write_results(path=full_path, mode='a', result=result)

