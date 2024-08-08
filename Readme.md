# Enviroment Setup.

Python Version 3.10.12

Install virtual environment.

Run `pip install virtualenv`

## Step 1 Clone the Repo

Run command `git clone <repo_url>`

## Step 2 Install venv

Navigate to your repo.
Run command `virtualenv .venv`

## Step 3 Activate virtual enviroment.

Run command `source .venv/bin/activate`

## Step 4 Installing python packages.

Run command `pip install -r requirements.txt`

## Step 5 Building docker image

Run command `docker build -t fetcher .`

## Step 6 Running docker image

Run command `docker run -it --rm -v $(pwd):/app fetcher <site_url> --metadata --mirror`

For exampel for www.google.com

Run command `docker run -it --rm -v $(pwd):/app fetcher https://www.google.com --metadata --mirror`

You can check the local folder with name `www.google.com`



