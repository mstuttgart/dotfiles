#!/bin/bash

# Ativa virtualenv
source .venv/bin/activate

# Atualizamos as dependencias
pip install -r requirements.txt

# Atualiza status das tarefas
./xmlrpc/odoo_xmlrpc.py move-tasks2test bot@multidadosti.com.br '!@#Botodoo!@#' --skip_confirmation

# Desativa o virtualenv
deactivate