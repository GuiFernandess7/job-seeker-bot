# Scraper/RPA Application for Developer Jr Job Openings

## Introduction

The **Job Scraper** is an automated web scraping application built using **Selenium** and **Python**. The application is designed to search for job listings on various websites such as Netvagas, LinkedIn, Indeed, and others, and store the results in a CSV file. It uses a headless Chrome browser running in a Docker container, ensuring that the scraping process is performed without opening a visible browser window. The application is containerized using **Docker** and orchestrated with **docker-compose**, providing a simple way to manage the environment and services.

## Features

- Scrapes job listings based on predefined queries from multiple job boards.
- Stores the results (job title and link) in a CSV file.
- Built with **Selenium** and **Python**, using a headless Chrome browser for scraping.
- Supports Docker for easy setup and execution.

## Requirements

Before running the application, ensure you have the following installed:

1. **Docker**: This is required to run the application in containers.
2. **Docker Compose**: To manage the multi-container setup for the application.
3. **Python (Optional)**: If you want to run the application without Docker.

### Installing Docker & Docker Compose

If you don't have Docker installed, follow these instructions based on your system:

- **Linux**: [Docker Installation Guide for Linux](https://docs.docker.com/engine/install/)
- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop)

Once Docker is installed, make sure Docker Compose is included in your installation or follow the official guide to install it separately: [Docker Compose Installation](https://docs.docker.com/compose/install/)

## Setting Up the Application

### 1. Clone the repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Build and Start the Docker Services

The project includes a `docker-compose.yml` file which defines the services needed for the application (the Python app and Selenium containers). To start the services, run the following command:

```bash
docker-compose up --build
```

This command will:

- Build the Docker images defined in the `Dockerfile`.
- Start the app, Selenium Hub, and Selenium Chrome Node containers.
- Expose the necessary ports for Selenium (4444) and the app (8000).

The `selenium/standalone-chrome` container will serve as the hub for Selenium WebDriver, while the `selenium/node-chrome` container acts as a browser node.

### 3. Run the Script

Once the containers are running, you can execute the scraping task by running the provided `run.sh` script:

```bash
./run.sh
```

This script will:

- Execute the Python script inside the `app` container using `pipenv`.
- The `pipenv run python -m src.main` command will run the main scraping logic.

The application will begin searching for jobs based on predefined queries and store the results in a CSV file under the `output` folder.

### 4. Check the Results

After the script completes, check the `output` folder in the project directory for the `output.csv` file. This file contains the job listings with their titles and links.

## File Structure

Here's an overview of the project file structure:

```
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image configuration
├── run.sh                    # Script to execute the job scraping task
├── main.py                   # Main Python script for job scraping
├── src/
│   └── services/
│       └── rpa/
│           └── bot.py        # Contains the bot logic for scraping
├── output/                   # Directory where CSV output is stored
│   └── output.csv            # Results from job scraping
└── .env                      # Environment variables for the application
```

## Explanation of the Docker Setup

- **App Service**: The Python application that runs the job scraping logic. It is built from the current directory (`.`) and runs on port `8000`.
- **Selenium Hub (selenium)**: The main Selenium server that coordinates browser nodes.
- **Selenium Chrome Node (chrome)**: A Selenium node running Chrome that executes the scraping tasks.

The containers are connected via a custom network (`selenium_network`) to allow communication between the app and the Selenium services.

## Environment Variables

You can configure various parameters in the `.env` file. Ensure that any necessary variables (such as database connection strings, if needed) are defined here. Currently, the `.env` file is empty but can be expanded as necessary.

## Troubleshooting

- **Selenium not starting**: Ensure that the Docker containers are properly started by checking the logs using `docker-compose logs selenium` or `docker-compose ps`.
- **Missing dependencies**: If any dependencies are missing when running the Python script, make sure they are listed in the `Pipfile` and install them using `pipenv install`.
- **Permissions**: Ensure the `run.sh` script has executable permissions. If necessary, run `chmod +x run.sh`.

## Demo

## Conclusion

This setup provides a fully containerized solution for scraping job listings from multiple websites. It simplifies running the application in a consistent environment using Docker, and all the job data will be saved in a CSV file for easy access.

Enjoy scraping job listings and automating your job search!
