import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from src.services.bot import RPAConcreteBuilder, JobSeekerBot

def write_results(path: str, mode: str = "w", result=None):
    with open(path, mode) as f:
        f.write(str(result) + '\n')

if __name__ == "__main__":
    job_queries = [
        "site:netvagas.com.br python junior developer"
        #"site:boards.greenhouse.io python junior developer",
        #"site:infojobs.com.br python junior",
        #"site:catho.com.br python junior",
        #"site:linkedin.com/jobs python junior",
        #"site:glassdoor.com.br python junior",
        #"site:indeed.com.br python junior",
    ]

    builder = RPAConcreteBuilder()
    bot = JobSeekerBot(builder)
    dest_folder = './data'
    full_path = os.path.join(dest_folder, 'results.txt')

    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        logging.info(f"Directory {dest_folder} created.")

    try:
        for query in job_queries:
            logging.info(f"Initializing search for: {query}")
            bot.build_full_featured_product('http://www.google.com', query)
            search_results = builder.product.get_search_results()

            if search_results:
                for result in search_results:
                    write_results(full_path, 'a', result)
                    logging.info(f"Result saved: {result}")

            else:
                logging.warning(f"Nothing found for query: {query}")

        logging.info("Search completed. All results have been saved to the file.")

    except Exception as e:
        logging.error(f"An error occured: {e}")

    finally:
        builder.driver_quit()
        logging.info("Drive closed.")

# https://www.youtube.com/watch?v=ECMbSLxLRbc