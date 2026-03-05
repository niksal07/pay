FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        netcat-openbsd \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]