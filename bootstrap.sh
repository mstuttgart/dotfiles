#!/bin/bash

# =============================================================================
# DOTFILES BOOTSTRAP SCRIPT
# =============================================================================
#
# Description: Minimal bootstrap script to prepare system for Ansible
#              and run the main provisioning playbook
#
# Author:      mstuttgart
# Repository:  https://github.com/mstuttgart/dotfiles
# License:     MIT
#
# This script:
# 1. Checks OS compatibility (Ubuntu 24.04 LTS)
# 2. Installs minimum dependencies (git, curl, python3, ansible)
# 3. Runs the main Ansible playbook
#
# Usage:
#   ./bootstrap.sh
#
# Requirements:
#   - Ubuntu 24.04 LTS
#   - Internet connection
#   - sudo privileges
#
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION VARIABLES
# =============================================================================

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/bootstrap-$(date +%Y%m%d-%H%M%S).log"

# =============================================================================
# COLOR CONSTANTS FOR OUTPUT FORMATTING
# =============================================================================

readonly RED='\e[31m'
readonly YELLOW='\e[33m'
readonly GREEN='\e[32m'
readonly BOLDBLUE="\e[1;34m"
readonly BOLDGREEN="\e[1;32m"
readonly ENDCOLOR="\e[0m"

# =============================================================================
# LOGGING AND OUTPUT FUNCTIONS
# =============================================================================

log_to_file() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

echo_nl() {
  echo ""
}

echo_print() {
  local message="$1"
  echo -e "${BOLDBLUE}=> $message ${ENDCOLOR}"
  log_to_file "INFO: $message"
}

echo_info() {
  local message="$1"
  echo -e "${BOLDGREEN}[info] $message ${ENDCOLOR}"
  log_to_file "INFO: $message"
}

echo_ok() {
  local message="$1"
  echo -e "${GREEN}[ok] $message ✔${ENDCOLOR}"
  log_to_file "SUCCESS: $message"
}

echo_warning() {
  local message="$1"
  echo -e "${YELLOW}[alert] $message ${ENDCOLOR}"
  log_to_file "WARNING: $message"
}

echo_error() {
  local message="$1"
  echo -e "${RED}[error] ✖ $message ✖ ${ENDCOLOR}"
  log_to_file "ERROR: $message"
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

check_return_code() {
  local exit_code="$1"
  local message="$2"
  
  if [ "$exit_code" -eq 0 ]; then
    echo_ok "$message"
  else
    echo_error "$message"
    exit 1
  fi
  echo_nl
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

check_os() {
  if [[ ! -f /etc/os-release ]]; then
    echo_error "Unsupported operating system"
    exit 1
  fi
  
  source /etc/os-release
  if [[ "$ID" != "ubuntu" ]] || [[ "$VERSION_ID" != "24.04" ]]; then
    echo_error "This script is designed for Ubuntu 24.04 LTS only"
    echo_error "Detected: $ID $VERSION_ID"
    exit 1
  fi
}

print_header() {
  clear
  echo -e "${BOLDBLUE}

██████╗  ██████╗ ████████╗███████╗██╗██╗     ███████╗███████╗
██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██║██║     ██╔════╝██╔════╝
██║  ██║██║   ██║   ██║   █████╗  ██║██║     █████╗  ███████╗
██║  ██║██║   ██║   ██║   ██╔══╝  ██║██║     ██╔══╝  ╚════██║
██████╔╝╚██████╔╝   ██║   ██║     ██║███████╗███████╗███████║
╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝

  ${YELLOW}BOOTSTRAP SCRIPT${BOLDGREEN}

" >&1
  echo_info "Log file: $LOG_FILE"
  echo_nl
}

print_footer() {
  echo -e "${BOLDGREEN}
  Bootstrap of dotfiles completed!${YELLOW}
  
  Check the log file for details: $LOG_FILE
" >&1
}

# =============================================================================
# INSTALLATION FUNCTIONS
# =============================================================================

update_system() {
  echo_print "Updating system packages"
  
  sudo apt update || {
    echo_error "Failed to update package list"
    return 1
  }
  
  sudo apt upgrade -y || {
    echo_error "Failed to upgrade packages"
    return 1
  }
  
  echo_ok "System updated successfully"
  echo_nl
}

install_dependencies() {
  echo_print "Installing minimum dependencies"
  
  local packages=(
    "git"
    "curl"
    "python3"
    "python3-pip"
    "python3-venv"
  )
  
  for package in "${packages[@]}"; do
    if command_exists "$package"; then
      echo_info "$package is already installed"
    else
      echo_info "Installing $package"
      sudo apt install -y "$package" || {
        echo_error "Failed to install $package"
        return 1
      }
    fi
  done
  
  echo_ok "Dependencies installed successfully"
  echo_nl
}

install_ansible() {
  echo_print "Installing Ansible"
  
  if command_exists ansible; then
    echo_warning "Ansible is already installed"
    ansible --version | head -1
    echo_nl
    return 0
  fi
  
  # Install via pip in virtual environment or system-wide
  sudo pip3 install ansible || {
    echo_error "Failed to install Ansible"
    return 1
  }
  
  echo_ok "Ansible installed successfully"
  echo_nl
}

run_ansible() {
  echo_print "Running Ansible playbook"
  
  if [[ ! -f "$SCRIPT_DIR/playbook.yml" ]]; then
    echo_error "playbook.yml not found in $SCRIPT_DIR"
    return 1
  fi
  
  cd "$SCRIPT_DIR" || exit 1
  
  ansible-playbook -i inventory/hosts.ini playbook.yml --ask-become-pass || {
    echo_error "Ansible playbook execution failed"
    return 1
  }
  
  echo_ok "Ansible playbook executed successfully"
  echo_nl
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main() {
  check_os
  print_header
  
  update_system
  install_dependencies
  install_ansible
  run_ansible
  
  print_footer
}

# Run main function
main "$@"
