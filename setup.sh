#!/bin/bash
# sudo apt install python3-dev ansible -y

ansible-playbook -i hosts playbooks/setup.yml --ask-become-pass -e 'ansible_python_interpreter=/usr/bin/python3'

# sudo apt purge ansible -y
# sudo apt autoremove -y