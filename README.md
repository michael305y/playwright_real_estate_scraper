A dockerized django based project designed to scrape real estate agent profiles across cities in USA. 
It processes each city in every state, identifying and extracting detailed profiles of real estate agents. 
It relies on one custom command `scraper.py`, 3 modules `main_scraper`, `Detailed_profile` and `DB_functions` modules for its operations. 

The custom command `scraper.py` initiates the script

##  seting up the project
1. create a folder called `project( preferred choice of naming)` `cd` into that directory, `create and  activate a venv`.
    . update the sytems packages `apt update` and insatll.
    . install git `apt install git` if git is not installed

2. clone the project  `git clone git@github.com:michael305y/playwright_real_estate_scraper.git`
3. `cd` playwright_real_estate_scraper
4. create and set up your `.env`(*should be in the root directory i.e. where manage.py is*) file for Django settings and configuration.
~~~
  DEBUG=1
  
  DJANGO_SECRET_KEY='your_secret_key_here'
  
  DJANGO_ALLOWED_HOSTS=your_allowed_hosts      (comma-separated domains or IPs, use * for development)
  
  DATABASE_NAME=your_database_name
  
  DATABASE_USERNAME=your_database_user
  
  DATABASE_PASSWORD=your_database_password
  
  DATABASE_HOST=your_database_host
  
  DATABASE_PORT=5432  # Default PostgreSQL port
  
  DJANGO_LOGLEVEL=info
  
  DJANGO_CSRF_TRUSTED_ORIGINS=https://your_domain
 ~~~
5. you can now build your image `docker compose build` once successsfull, run or start a container with `docker compose up`.
6. 




