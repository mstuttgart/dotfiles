#!/bin/bash -e

source colors.sh

# Set script to stop if any command fail
# set -e

source setup-apps.sh
check_return_code $? "setup-apps.sh"

source setup-environment.sh
check_return_code $? "setup-environment.sh"

source setup-dotfiles.sh
check_return_code $? "setup-dotfiles.sh"
