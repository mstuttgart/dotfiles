#!/bin/bash
#
# Config created by mstuttgart https://www.github.com/mstuttgart/dotfiles
# Copyright (C) 2023 Michell Stuttgart
#

function new_line { echo -e ""; }
function print { echo -e "\033[1;32m=> $1\033[0m"; }
function msg_checking { echo -e "\033[1;32m[ok] $1 ✔\033[0m"; }
function msg_update { echo -e "\033[1;33m[update] $1 \033[0m"; }
function msg_install { echo -e "\033[1;33m[installing] $1 \033[0m"; }
function msg_ok { echo -e "\033[1;32m[installed] $1 ✔\033[0m"; }
function msg_info { echo -e "\033[0;32m[info] $1 \033[0m"; }
function msg_alert { echo -e "\033[1;31m[alert] ✖ $1 ✖\033[0m"; }

function check_return_code () {

    # The $1 is $?, the result of last command
    if [ $1 -eq 0 ]
    then
        msg_ok "$2"
    else
        msg_alert "$2"
        exit 1
    fi

    new_line
}

config_dir="$HOME/.config"
fonts_dir="$HOME/.fonts"
icons_dir="$HOME/.icons"
local_bin_dir="$HOME/.local/bin"

Apps=(
  # cli
  "p7zip"
  "p7zip-full"
  "p7zip-rar"
  "rar"
  "software-properties-common"
  "ubuntu-restricted-extras"
  "unace-nonfree"
  "unrar"
  "uuid-runtime"
  "wget"
  "curl"
  "net-tools"
#  "exa"
  "bat"
#  "btop"
  "pwgen"
  "git"
  "tig"
  "gpick"
  "gimp"
  "libreoffice"
  "openssh-server"
  "neofetch"
#  "zoxide"
#  "newsboat"
#  "xclip"
  "poedit"
#  "evince"
#  "fzf"
#  "asdf"

  # fonts
  "fonts-clear-sans"
  "fonts-firacode"
  "fonts-inter"

  # i3
  # "i3"
#  "i3lock"
#  "netctl"
#  "nitrogen"
#  "compton"
#  "rofi"
#  "light"           # brightness control
#  "suckless-tools"
#  "hsetroot"
#  "fonts-noto"
#  "fonts-mplus"
#  "xsettingsd"
#  "netctl"
#  "lxappearance"
#  "polybar"
#  "playerctl"
#  "numlockx"
#  "acpi"         # battery info

  # ranger
#  "ranger"
#  "w3m-img"
#  "ffmpegthumbnailer"
#  "highlight"
#  "unrar"
#  "unzip"
#  "mediainfo"
#  "mvp"

  # Programming
  "build-essential"
  "cmake"
  "g++"
  "libsqlite3-dev"
  "llvm"
  "make"

  # python
  "python3-dev"
  "python3-pip"
  "python3-venv"

  # pyenv
  "build-essential"
  "libssl-dev"
  "zlib1g-dev"
  "libbz2-dev"
  "libreadline-dev"
  "libsqlite3-dev"
  "curl"
  "libncursesw5-dev"
  "xz-utils"
  "tk-dev"
  "libxml2-dev"
  "libxmlsec1-dev"
  "libffi-dev"
  "liblzma-dev"

  # nvim
  "exuberant-ctags"
  "ncurses-term"
  "curl"
  "ripgrep"
  "fd-find"

  # apps
  "gpick"
  "flameshot"
  "gdebi"
  "libreoffice"
  "openssh-server"
  "poedit"
  "filezilla"
#  "firefox"

  # themes
  "arc-theme"
  "font-manager"
  "fonts-powerline"

)

msg_info "Create basic folders"

print "Create $config_dir"
mkdir -p $config_dir

print "Create $fonts_dir"
mkdir -p $fonts_dir

print "Create $local_bin_dir"
mkdir -p $local_bin_dir

print
msg_checking
new_line

for app in "${Apps[@]}"; do
    msg_install "$app"
    # Install app
    sudo apt install $app -y

    # The $? get result of last command
    check_return_code $? $app
done

# # Add user to video group to control brightness
# sudo chmod +s /usr/bin/light
#
#
# # Install neovim
# msg_install "Install NVIM"
#
# wget https://github.com/neovim/neovim/releases/download/v0.9.0/nvim.appimage
#
# mkdir -p $local_bin_dir
# mv -f nvim.appimage $local_bin_dir/nvim
# chmod +x $local_bin_dir/nvim
#
# msg_checking
# new_line
#
# # Install packer
# msg_install "Install Packer"
#
# git clone --depth 1 https://github.com/wbthomason/packer.nvim ~/.local/share/nvim/site/pack/packer/start/packer.nvim
#
# msg_checking
# new_line
#
# # Install node version manager (nvm)
# msg_install "Install nvm"
# curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
# msg_checking
#
# msg_install "Install nodejs"
# nvm install --lts
# msg_checking
#
# new_line
#
# # Install ncspot
# msg_install "Install ncspot"
# wget https://github.com/hrkfdn/ncspot/releases/download/v0.13.1/ncspot-v0.13.1-linux-arm64.tar.gz
# tar xvzf ncspot-v0.13.1-linux-arm64.tar.gz -C $local_bin_dir
# rm -rf ncspot-v0.13.1-linux-arm64.tar.gz
#
# msg_checking
# new_line
#
# # Install pyenv
# msg_install "Install pyenv and pyenv-virtualenv"
# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# git clone https://github.com/pyenv/pyenv-virtualenv.git  ~/.pyenv/plugins/pyenv-virtualenv
# msg_checking
#
# new_line

msg_info "Done!"
