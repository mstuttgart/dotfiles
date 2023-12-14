#!/bin/bash

# Ativa virtualenv
source .venv/bin/activate

# Atualizamos as dependencias
pip install -r requirements.txt

# Atualiza status das tarefas
./xmlrpc/make_backup.sh

# Desativa o virtualenv
deactivate