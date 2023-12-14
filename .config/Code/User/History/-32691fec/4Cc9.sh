#!/bin/bash

ansible-playbook -i environments/production_6 --vault-password-file=environments/production_6/vault.key playbooks/update_odoo.yml -u ubuntu --extra-vars "deploy_update_dbs=false slack_enable_notification=true"
