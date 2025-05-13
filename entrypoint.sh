#!/bin/bash
echo ">> Aguardando banco ficar pronto..."
sleep 5

echo ">> Aplicando migracae..."
flask db upgrade

echo ">> Populando banco ficticio..."
python -m app.scripts.popular_db

echo ">> Iniciando aplicação Flask..."
exec flask run --host=0.0.0.0 --port=5000

