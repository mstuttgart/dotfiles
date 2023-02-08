#!/bin/bash

# script based in: https://github.com/sloria/dotfiles/blob/master/bin/dot-update

# Update local dev environment using ansible-playbook.
# Optionally pass role names.
set -e

if [[ $# -eq 0 ]]; then
  # Run all roles
  echo "Updating local dev environment..."
  ansible-playbook -i inventory.ini playbooks/setup.yml --ask-become-pass --skip-tags "optional"

else
  echo "Updating local dev environment... (--tags $@)"
  ansible-playbook -i inventory.ini playbooks/setup.yml --ask-become-pass --tags $@

fi

# Display a notification
notify-send 'Update complete' 'Successfully updated dev environment'
