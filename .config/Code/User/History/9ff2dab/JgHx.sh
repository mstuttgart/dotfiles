#!/bin/bash

# Utiliza em casos onde desejamos atualizar o banco de dados
# de producao com o conteudo da main

source colors.sh

# Altera para diretorio de scripts de infra-multierp
cd infra-multierp/

# Atualizamos o repositorio, de modo
# a garantir que ele esteja sempre atualizado
git fetch -p
git reset --hard origin/main

# Ativa virtualenv
source .venv/bin/activate

# Atualizamos as dependencias
pip install -r requirements.txt

# Inicia atualização do Producao e atualizacao dos banco de dados
# Os dois scritps serao eexecutados em background e em paralelo
# Como sao servidores diferentes (odoo e postgresql), não haverá conflito
source bin/prod-1-update-all.sh > prod-1-update-all.log 2>&1 &
source bin/prod-2-update-all.sh > prod-2-update-all.log 2>&1 &
source bin/prod-3-update-all.sh > prod-3-update-all.log 2>&1 &
source bin/prod-4-update-all.sh > prod-4-update-all.log 2>&1 &
source bin/prod-5-update-all.sh > prod-5-update-all.log 2>&1

# Comando para aguardar os comandos acima serem executados
# Ambos estao sendo executados em pararelo, entao precisamos
# aguardar a conclusao para prosseguir com o processo de atualização
wait

# Desativa o virtualenv
deactivate

# Volta para diretorio raiz
cd ..
