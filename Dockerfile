FROM python:3.9-slim

# Set working directory
WORKDIR /prediction-api
COPY /app ./app
COPY /data ./data
COPY requirements.txt .
COPY config.ini ./app/config.ini
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5555", "app.prediction:app"]