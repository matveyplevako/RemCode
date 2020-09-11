FROM python:3
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y install gcc mono-mcs && rm -rf /var/lib/apt/lists/*
RUN pip install redis
COPY worker.py .
CMD python worker.py
