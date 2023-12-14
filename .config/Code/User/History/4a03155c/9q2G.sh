#!/bin/bash

source data/db_list.sh

ansible-playbook -i environments/production_6 --vault-password-file=environments/production_6/vault.key playbooks/update_odoo.yml -u ubuntu --extra-vars "deploy_update_dbs=false slack_enable_notification=true"

sleep 3m

for db_name in "${PRODUCAO_6_DBs[@]}"; do
  ansible-playbook -i environments/production_6 --vault-password-file=environments/production_6/vault.key playbooks/update_all.yml -u ubuntu --extra-vars "deploy_update_dbs=true db_to_update=$db_name slack_enable_notification=true"
  sleep 3m
done
