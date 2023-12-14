#!/bin/bash

# Altera para diretorio de scripts de infra-multierp
cd ~/infra-multierp

# Atualizamos o repositorio, de modo
# a garantir que ele esteja sempre atualizado
git fetch
git reset --hard origin/main

# Ativa virtualenv
source .venv/bin/activate

# Lista tarefas aprovadas no Code Review
./xmlrpc/odoo_xmlrpc.py list-tasks2deploy bot@multidadosti.com.br '!@#Botodoo!@#'

# Desativa o virtualenv
deactivate

# Retorna para repositorio raiz
cd
