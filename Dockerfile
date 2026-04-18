FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static files (doesn't need database)
RUN python manage.py collectstatic --noinput

# Create startup script that runs migrations THEN starts the server
RUN echo '#!/bin/bash\n\
echo "Waiting for database..."\n\
sleep 3\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
echo "Creating superuser..."\n\
python create_superuser.py\n\
echo "Starting Gunicorn..."\n\
gunicorn elgonnova.wsgi:application --bind 0.0.0.0:8000' > /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]