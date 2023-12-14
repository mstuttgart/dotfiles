#!/bin/bash

ansible-playbook -i environments/qa --vault-password-file=environments/qa/vault.key playbooks/update_odoo.yml -u ubuntu --extra-vars "deploy_update_dbs=false slack_enable_notification=true" -v
