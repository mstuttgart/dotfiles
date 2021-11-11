#!/bin/bash

source .venv/bin/activate

ansible-playbook -i hosts playbooks/setup.yml --ask-become-pass -e 'ansible_python_interpreter=/usr/bin/python3'

deactivate