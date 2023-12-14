#!/bin/bash

# Muda para o diretorio do Odoo de Release
cd multierp/

# # Ativa virtualenv
source .venv/bin/activate

# Atualiza branch do projeto
git fetch
git reset --hard origin/main

# Carrega novos submodulos
git submodule init
git submodule update

# Voltamos para a branch 'develop' para fazer o reset delas.
# Isso garante que o script continuara funcionando caso o historico
# da 'develop' seja alterado
manager git checkout develop
manager git foreach 'git reset --hard origin/develop'

# Atualizamos a branch de QA
manager release qa

# Desativa o virtualenv
deactivate

# Voltamos para diretorio raiz
cd ..

# ----------------------------------------------------------

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

# Inicia atualização do QA
./bin/qa-update-all.sh

# Atualiza status das tarefas
./xmlrpc/odoo_xmlrpc.py move-tasks2test bot@multidadosti.com.br '!@#Botodoo!@#' --skip_confirmation

# Desativa o virtualenv
deactivate

# Retorna para repositorio raiz
cd ..
