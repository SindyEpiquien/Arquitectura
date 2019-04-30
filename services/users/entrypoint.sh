#!/bin/sh

echo "Esperando a postgres..."

while ! nc -z users-db 5432; do
  sleep 0.1
done

echo "PostgreSQL iniciado"

python manage.py run -h 0.0.0.0
