#!/bin/bash

source colors.sh

# Create bin path ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

new_line
msg "Create folder to store executables and appImage files"
print "Create ~/.local/bin folder"

mkdir -p ~/.local/bin
check_return_code $?

# Install dependencies ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print "Installing dependencies"
new_line

apt_apps=(
    "build-essential"
    "make"
    "cmake"
    "dh-make"
    "make"
    "curl"
    "g++"
    "wget"
    "python3-dev"
    "python3-pip"
    "python3-venv"
    "p7zip"
    "p7zip-full"
    "p7zip-rar"
    "unrar"
    "rar"
    "unace-nonfree"
    "ubuntu-restricted-extras"
)

for app in "${apt_apps[@]}"; do
    msg_install "$app"
    
    # Install app
    sudo apt install $app -y
    
    # The $? get result of last command
    check_return_code $? $app
    
done

# Update OS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print "Update Operational System"
new_line

msg_update "apt update"
sudo apt update
check_return_code $? "apt update"

msg_update "apt upgrade"
sudo apt upgrade -y
check_return_code $? "apt upgrade"

msg_update "apt autoremove"
sudo apt autoremove -y
check_return_code $? "apt autoremove"

msg "Install done: `date +%d-%m-%y_%H:%M:%S`"

new_line
