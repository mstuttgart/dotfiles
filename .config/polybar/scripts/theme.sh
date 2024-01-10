#!/bin/bash
#

POLYBAR_THEME_DIR="$HOME/.config/polybar/themes"

function rofi_switch_theme_menu {
	echo -e "Ayu Light\nAyu Dark\nAyu Mirage\nEverforest Light\nEverforest Dark\nGruvbox Dark\nGruvbox Material Dark\nNord\nTokyo Night" | rofi -font "JetBrainsMono Nerd Font 11" -show drun -show-icons -width 20 -dmenu -i
}

function create_symlink {
	ln -sf "$POLYBAR_THEME_DIR/$1.ini" "$POLYBAR_THEME_DIR/colors.ini"
	bash "$HOME/.config/polybar/launch.sh"
}

CHOSEN=$(rofi_switch_theme_menu)

if [[ $CHOSEN = "Ayu Light" ]]; then
  create_symlink 'ayu-light'

elif [[ $CHOSEN = "Ayu Dark" ]]; then
  create_symlink 'ayu-dark'

elif [[ $CHOSEN = "Ayu Mirage" ]]; then
  create_symlink 'ayu-mirage'

elif [[ $CHOSEN = "Everforest Light" ]]; then
  create_symlink 'everforest-light'

elif [[ $CHOSEN = "Everforest Dark" ]]; then
  create_symlink 'everforest-dark'

elif [[ $CHOSEN = "Gruvbox Dark" ]]; then
  create_symlink 'gruvbox-dark'

elif [[ $CHOSEN = "Gruvbox Material Dark" ]]; then
  create_symlink 'gruvbox-material-dark'

elif [[ $CHOSEN = "Nord" ]]; then
  create_symlink 'nord'

elif [[ $CHOSEN = "Tokyo Night" ]]; then
  create_symlink 'tokyo-night'
fi
