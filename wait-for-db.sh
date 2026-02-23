#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z db 3306; do
  sleep 1
done

echo "MySQL started!"
echo "Running migrations..."
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

echo "Seeding admin..."
python create_admin.py

python run.py   