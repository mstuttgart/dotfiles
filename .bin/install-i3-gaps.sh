#!/bin/bash
#
# Config created by mstuttgart https://www.github.com/mstuttgart/dotfiles
# Copyright (C) 2023 Michell Stuttgart
#

# Install dependencies
sudo apt install meson asciidoc

sudo apt install libxcb1-dev libxcb-keysyms1-dev libpango1.0-dev \
libxcb-util0-dev libxcb-icccm4-dev libyajl-dev \
libstartup-notification0-dev libxcb-randr0-dev \
libev-dev libxcb-cursor-dev libxcb-xinerama0-dev \
libxcb-xkb-dev libxkbcommon-dev libxkbcommon-x11-dev \
autoconf libxcb-xrm0 libxcb-xrm-dev automake libxcb-shape0-dev

# create build dir
cd ~
mkdir /tmp/build-gaps
cd /tmp/build-gaps

# Clone repo
git clone https://www.github.com/Airblader/i3 i3-gaps

cd i3-gaps

# Build gaps
#git checkout gaps && git pull
#meson -Ddocs=true -Dmans=true ../build
#meson compile -C ../build
#sudo meson install -C ../build

mkdir -p build && cd build
meson ..
ninja

cd ~
