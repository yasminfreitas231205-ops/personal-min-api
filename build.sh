#!/usr/bin/env bash
# exit on error
set -o errexit

# Instala as dependências do projeto
pip install -r requirements.txt

# Reúne os arquivos estáticos na pasta STATIC_ROOT
python manage.py collectstatic --no-input

# Aplica as estruturas de tabela no banco PostgreSQL da nuvem
python manage.py migrate