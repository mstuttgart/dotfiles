#!/bin/bash
#
# Config created by mstuttgart https://www.github.com/mstuttgart/dotfiles
# Copyright (C) 2023 Michell Stuttgart
#

# get from: https://i3wm.org/docs/repositories.html
#
/usr/lib/apt/apt-helper download-file https://debian.sur5r.net/i3/pool/main/s/sur5r-keyring/sur5r-keyring_2023.02.18_all.deb keyring.deb SHA256:a511ac5f10cd811f8a4ca44d665f2fa1add7a9f09bef238cdfad8461f5239cc4

sudo apt install ./keyring.deb

# repo for ubuntu 22.04 jammy
echo "deb http://debian.sur5r.net/i3/ jammy universe" | sudo tee /etc/apt/sources.list.d/sur5r-i3.list

sudo apt update
sudo apt install i3
