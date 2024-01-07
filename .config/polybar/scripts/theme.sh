#!/bin/bash
#

POLYBAR_THEME_DIR="$HOME/.config/polybar/themes"

function rofi_switch_theme_menu {
	echo -e "Ayu Light\nAyu Dark\nAyu Mirage\nEverforest Light\nEverforest Dark\nNord" | rofi -font "JetBrainsMono Nerd Font 11" -show drun -show-icons -width 20 -dmenu -i
}

function create_symlink {
	ln -sf "$POLYBAR_THEME_DIR/$1.ini" "$POLYBAR_THEME_DIR/colors.ini"
	bash "$HOME/.config/polybar/launch.sh"
}

CHOSEN=$(rofi_switch_theme_menu)

if [[ $CHOSEN = "Ayu Light" ]]; then
  create_symlink 'ayu-light'
	# ln -sf "$POLYBAR_THEME_DIR/ayu-light.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

elif [[ $CHOSEN = "Ayu Dark" ]]; then
  create_symlink 'ayu-dark'
	# ln -sf "$POLYBAR_THEME_DIR/ayu-dark.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

elif [[ $CHOSEN = "Ayu Mirage" ]]; then
  create_symlink 'ayu-mirage'
	# ln -sf "$POLYBAR_THEME_DIR/ayu-mirage.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

elif [[ $CHOSEN = "Everforest Light" ]]; then
  create_symlink 'everforest-light'
	# ln -sf "$POLYBAR_THEME_DIR/everforest-light.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

elif [[ $CHOSEN = "Everforest Dark" ]]; then
  create_symlink 'everforest-dark'
	# ln -sf "$POLYBAR_THEME_DIR/everforest-dark.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

elif [[ $CHOSEN = "Nord" ]]; then
  create_symlink 'nord'
	# ln -sf "$POLYBAR_THEME_DIR/everforest-dark.ini" "$POLYBAR_THEME_DIR/colors.ini"
	# bash "$HOME/.config/polybar/launch.sh"

fi
