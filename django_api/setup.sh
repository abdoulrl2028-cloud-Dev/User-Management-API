#!/bin/bash
set -e

echo "Executando migrações do banco de dados..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Setup completo!"
