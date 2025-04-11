FROM python:3.10

# ensure logs are flushed immediately
ENV PYTHONUNBUFFERED=1

# install minio and paho-mqtt
RUN pip3 install minio paho-mqtt

# cp subscribe_and_publish.py to /app
COPY subscribe_and_republish.py /app/subscribe_and_republish.py

# set working directory
WORKDIR /app

# run subscribe_and_republish.py
CMD ["python3", "subscribe_and_republish.py"]