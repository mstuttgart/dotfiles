#!/bin/bash

# Ativa virtualenv
source .venv/bin/activate

# Lista tarefas para hotfix
./xmlrpc/odoo_xmlrpc.py list-tasks2deploy bot@multidadosti.com.br '!@#Botodoo!@#' --hotfix

# Desativa o virtualenv
deactivate