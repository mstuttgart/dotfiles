#!/bin/bash


# Altera para diretorio de scripts de infra-multierp
cd infra-multierp/

# Atualizamos o repositorio, de modo
# a garantir que ele esteja sempre atualizado
git fetch -p
git reset --hard origin/main

# Ativa virtualenv
source .venv/bin/activate

# Atualiza status das tarefas
./xmlrpc/make_backup.sh

# Desativa o virtualenv
deactivate