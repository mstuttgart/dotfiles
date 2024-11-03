#!/bin/bash

  i3wm_pkg=(
    "acpi"
    "arandr"
    "autorandr"
    "dex"
    "dmenu"
    "dunst"
    "galculator"
    "gsimplecal"
    "i3-wm"
    "i3lock"
    "jq"
    "lxappearance"
    "neofetch"
    "nitrogen"
    "numlockx"
    "picom"
    "playerctl"
    "polybar"
    "rofi"
    "sysstat"
    "thunar"
    "thunar-archive-plugin"
    "thunar-volman"
    "tumbler"
    "unzip"
    "viewnior"
    "xarchiver"
    "xbindkeys"
    "xdg-user-dirs-gtk"
    "xed"
    "zip"
    "ttf-jetbrains-mono-nerd"
    "ttf-sourcecodepro-nerd"
 "gvfs"
    "gvfs-afc"
    "gvfs-gphoto2"
    "gvfs-mtp"
    "gvfs-nfs"
    "gvfs-smb"
  )

  for app in "${i3wm_pkg[@]}"; do


    # Install app
    sudo pacman -S "$app" --needed --noconfirm


  done

