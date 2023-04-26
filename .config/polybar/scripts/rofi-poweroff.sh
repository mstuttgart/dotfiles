#!/bin/bash

rofi_poweroff_menu () {
    echo -e "Logout\nReboot\nShutdown" | rofi -font "FiraCode Nerd Font 11" -show drun -show-icons -width 20 -l 3 -dmenu -i
}

chosen=$(rofi_poweroff_menu)

if [[ $chosen = "Logout" ]]; then
  systemctl logout
elif [[ $chosen = "Shutdown" ]]; then
	systemctl poweroff
elif [[ $chosen = "Reboot" ]]; then
	systemctl reboot
fi
