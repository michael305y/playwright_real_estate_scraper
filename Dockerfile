# FROM python:3.11-slim

# RUN pip install --upgrade pip && \
#     pip install playwright==1.49.1 && \
#     playwright install --with-deps


## ===== FOR PRODUCTION =====================
# FROM python:3.11-slim
FROM slim:latest

ENV PYTHONBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1 

WORKDIR /app

# RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


RUN pip install --upgrade pip && \
    pip install playwright==1.49.1 && \
    playwright install --with-deps

COPY . .

RUN python manage.py collectstatic --noinput

## runs our scrapper
# RUN python manage.py run_scraper_2    


EXPOSE 8000

# CMD [ "manage.py", "gunicorn" , "python", 'custom_command']
# CMD [ "python", "manage.py" , "custom_command", "0.0.0.0:8000" ]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "real_estate_crawler_project.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "real_estate_scraper_project.wsgi:application"]

