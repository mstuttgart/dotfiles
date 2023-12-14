#!/bin/bash

# Ativa virtualenv
source .venv/bin/activate

# Lista tarefas aprovadas no Code Review
./xmlrpc/odoo_xmlrpc.py list-tasks2deploy bot@multidadosti.com.br '!@#Botodoo!@#'

# Desativa o virtualenv
deactivate