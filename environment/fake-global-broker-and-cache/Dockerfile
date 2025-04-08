FROM python:3.10

# ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1

# cp subscribe_and_publish.py to /app
COPY subscribe_and_publish.py /app/subscribe_and_publish.py

# set working directory
WORKDIR /app

# run subscribe_and_publish.py
CMD ["python3", "subscribe_and_publish.py"]