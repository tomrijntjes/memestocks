# Memestocks

Airflow based scraper of investing subreddits.

## Getting Started

### Requirements

- docker
- docker-compose

### Running Locally

Copy and rename `secrets.env-template` to `secrets.env` and add a client ID, client secret and user agent. The Python Reddit API Wrapper offers a [getting started](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) guide to get these credentials.

Run `docker-compose up --build` from the root directory. Open `localhost:8080` to view the Airflow UI.