#!/bin/bash

# Ativa virtualenv
source .venv/bin/activate

# Atualiza status das tarefas
./xmlrpc/odoo_xmlrpc.py move-tasks2done bot@multidadosti.com.br '!@#Botodoo!@#' --skip_confirmation

# Desativa o virtualenv
deactivate