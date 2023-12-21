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

function check_return_code() {

	# The $1 is $?, the result of last command
	if [ $1 -eq 0 ]; then
		msg_ok "$2"
	else
		msg_alert "$2"
		exit 1
	fi

	new_line
}

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
	"pwgen"
	"git"
	"tig"
	"gpick"
	"gimp"
	"libreoffice"
	"openssh-server"
	"neofetch"
	"imagemagick"
	"xclip"
	"poedit"
	"pass"
	"fzf"

	# i3
	"i3"
	"i3lock"
	"netctl"
	"nitrogen"
	"compton"
	"rofi"
	"light" # brightness control
	"hsetroot"
	"fonts-noto"
	"fonts-mplus"
	"xsettingsd"
	"netctl"
	"lxappearance"
	"polybar"
	"playerctl"
	"numlockx"
	"acpi" # battery info
	"gsimplecal"

	# ranger
	#	"ranger"
	#	"w3m-img"
	#	"ffmpegthumbnailer"
	#	"highlight"
	#	"unrar"
	#	"unzip"
	#	"mediainfo"
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
	"firefox"

	# themes
	# "arc-theme"
	#	"font-manager"
	#	"fonts-powerline"
)

msg_info "Create basic folders"

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

msg_info "Done!"
