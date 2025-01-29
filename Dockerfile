FROM python:3.11-slim


ENV PYTHONBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip && \
    pip install playwright==1.49.1 && \
    playwright install --with-deps

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "real_estate_scraper_project.wsgi:application"]

