#!/bin/bash

# Atualizamos as dependencias
pip install -r requirements.txt

# Ativa virtualenv
source .venv/bin/activate

# Atualiza status das tarefas
./xmlrpc/make_backup.sh

# Desativa o virtualenv
deactivate