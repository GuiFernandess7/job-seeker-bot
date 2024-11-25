import logging
from dotenv import load_dotenv
import csv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from src.services.rpa.bot import RPAConcreteBuilder, JobSeekerBot

import os

def write_results(path: str, mode: str = "w", result=None):
    file_exists = os.path.isfile(path)

    with open(path, mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(['Job Title', 'Link'])

        writer.writerow(result)
        logging.info(f'[DATA] - {result} written to CSV')

if __name__ == "__main__":
    job_queries = [
        """ site:netvagas.com.br "Desenvolvedor Jr" "remoto" """,
        """ site:netvagas.com.br "Desenvolvedor Junior" "remoto" """,
        """ site:netvagas.com.br "Desenvolvedor Python Jr" "remoto" """,
        """ site:netvagas.com.br "Junior Python Developer" """,

        """site:https://jobs[.]lever[.]co "Junior Developer" "remote" -"remote only in the US""",
        """site:https://jobs[.]lever[.]co "Junior Developer" "remote" """,
        """site:https://jobs[.]lever[.]co "Junior Python Developer" "remote" """,

        """ site:boards[.]greenhouse[.]io "Junior Developer" "remote" -"remote only in the US" """,
        """ site:boards[.]greenhouse[.]io "Junior Developer" "remote" """,
        """ site:boards[.]greenhouse[.]io "Junior Python Developer" "remote" """,
        """ site:boards[.]greenhouse[.]io "Python Developer" "remote" """,

        """ site:jobs[.]ashbyhq[.]com "Junior Developer" "remote" -"remote only in the US" """,
        """ site:jobs[.]ashbyhq[.]com "Junior Developer" "remote" """,
        """ site:jobs[.]ashbyhq[.]com "Junior Python Developer" "remote" """,
        """ site:jobs[.]ashbyhq[.]com "Junior Developer" "remote" """,

        """ site:jobs[.]jobvite[.]com "Junior Developer" "remote" -"remote only in the US" """,
        """ site:jobs[.]jobvite[.]com "Junior Developer" "remote" """,
        """ site:jobs[.]jobvite[.]com "Junior Python Developer" "remote" """,

        """ site:myworkdayjobs[.]com "Junior Developer" "remote" -"remote only in the US" """
        """ site:myworkdayjobs[.]com "Junior Developer" "remote" """
        """ site:myworkdayjobs[.]com "Junior Python Developer" "remote" """
    ]

    all_results = []
    #DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
    dest_folder = './output'
    full_path = os.path.join(dest_folder, 'output.csv')

    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
        logging.info(f"Directory {dest_folder} created.")

    builder = RPAConcreteBuilder(headless=True, selenium_url="http://selenium:4444/wd/hub")
    driver = builder.get_driver()
    bot = JobSeekerBot(driver)

    try:
        logging.info(f"Initializing search for: {job_queries[0]}")
        search_results = bot.search_and_extract(job_queries)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    for result in search_results:
        write_results(path=full_path, mode='a', result=result)

#"site:netvagas.com.br python junior developer",
#"site:boards.greenhouse.io python junior developer"
#"site:infojobs.com.br python junior",
#"site:catho.com.br python junior",
#"site:linkedin.com/jobs python junior",
#"site:glassdoor.com.br python junior",
#"site:indeed.com.br python junior",
#"site:netvagas.com.br junior developer",
#"site:boards.greenhouse.io junior developer",
#"site:infojobs.com.br junior developer",
#"site:catho.com.br junior developer remoto",
#"site:linkedin.com/jobs junior developer",
#"site:glassdoor.com.br junior developer",
#"site:indeed.com.br junior developer remoto"