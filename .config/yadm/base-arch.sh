#!/bin/bash

echo "[START]: general-packages installation..."

sudo pacman -Syu

sudo pacman -S xorg xorg-apps xorg-xinit xorg-xlsfonts xdotool xclip xsel

# XORG_PKG=(
#   xorg
#   xorg-apps
#   xorg-xinit
#   xorg-xlsfonts
#   xdotool
#   xclip
#   xsel
# )

sudo pacman -S --neeeded --noconfirm \
  dbus \  # Message bus used by many applications
intel-ucode \ # Microcode update files for Intel CPUs
fuse2 \     # Interface for programs to export a filesystem to the Linux kernel
lshw \      # Provides detailed information on the hardware of the machine
powertop \  # A tool to diagnose issues with power consumption and power management
inxi \      # Full featured CLI system information tool
acpi \      # Client for battery, power, and thermal readings

base-devel \ # Basic tools to build Arch Linux packages
git \    # Distributed version control system
zip \    # Compressor/archiver for creating and modifying zipfiles
unzip \  # For extracting and viewing files in .zip archives
htop \   # Interactive CLI process viewer
tree \   # A directory listing program

dialog \     # A tool to display dialog boxes from shell scripts
reflector \  # Script to retrieve and filter the latest Pacman mirror list
bash-completion \# Programmable completion for the bash shell

iw \  # CLI configuration utility for wireless devices
wpa_supplicant \ # A utility providing key negotiation for WPA wireless networks
tcpdump \    # Powerful command-line packet analyzer
mtr \        # Combines the functionality of traceroute and ping into one tool
net-tools \  # Configuration tools for Linux networking
conntrack-tools \ # Userspace tools to interact with the Netfilter tracking system
ethtool \  # Utility for controlling network drivers and hardware
wget \     # Network utility to retrieve files from the Web
rsync \    # File copying tool for remote and local files
socat \    # Multipurpose socket relay
openbsd-netcat \ # Netcat program. OpenBSD variant.
axel \  # Light command line download accelerator
bind \  # I use dig utility for DNS resolution from this package

echo "[FINISHED]: general-packages installation"
