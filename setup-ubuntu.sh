#!/bin/bash

export Off=$'\e[0m'
export White=$'\e[1;37m'
export BlueBG=$'\e[1;44m'
export Yellow=$'\e[1;33m'

# Create bin path
mkdir -p ~/.local/bin

echo ""
echo "${Yellow}Install Build Essentials ${Off}"
echo ""

sudo apt install build-essential make cmake -y
sudo apt install dh-make make -y
sudo apt install curl -y
sudo apt install g++ -y
sudo apt install libsqlite3-dev -y
sudo apt install wget -y

echo ""
echo "${Yellow}Install Python and Pip ${Off}"
echo ""

# Install Python dependencies
sudo apt install python3-dev -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y


echo -e ""
echo -e "${Yellow}Install Git tools"
echo -e ""

sudo apt install git git-core tig -y

echo -e ""
echo -e "${Yellow} Install File Compression Libs ${Off}"
echo -e ""

sudo apt install p7zip p7zip-full p7zip-rar unrar rar unace-nonfree -y

echo -e ""
echo -e "${Yellow} Install Ubuntu Restricted Extras ${Off}"
echo -e ""

sudo apt install ubuntu-restricted-extras -y

echo -e ""
echo -e "${Yellow} Download and Install Google Chrome ${Off}"
echo -e ""

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
rm -f google-chrome-stable_current_amd64.deb

echo -e ""
echo -e "${Yellow} Install VsCode ${Off}"
echo -e ""

curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'

# Configurações adicionais do vscode
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf
sudo sysctl -p

echo -e ""
echo -e "${Yellow}Install Tree Directory Viewer ${Off}"
echo -e ""

sudo apt install tree -y

echo -e ""
echo -e "${Yellow}Install Neofecth ${Off}"
echo -e ""

sudo apt install neofetch -y

echo -e ""
echo -e "${Yellow}Install htop ${Off}"
echo -e ""

sudo apt install htop -y

#--------------------------------------------------
# Update System
#--------------------------------------------------

echo -e ""
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e " ${White}${BlueBG}         -= Update System =-                             ${Off}"
echo -e " ${White}${BlueBG}                                                         ${Off}"
echo -e ""

sudo apt update
sudo apt autoremove -y

echo -e ""
echo -e "${Yellow} Install done: `date +%d-%m-%y_%H:%M:%S`"

neofetch
