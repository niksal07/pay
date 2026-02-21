FROM python:3.12-slim

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install mysqlclient
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]


