#!/bin/bash
#
# Config created by mstuttgart https://www.github.com/mstuttgart/dotfiles
# Copyright (C) 2023 Michell Stuttgart
#
# sudo apt install zsh curl

cd "$HOME"

# Install oh-my-zsh


# sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


# Install plugins
git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"

git clone https://github.com/zsh-users/zsh-syntax-highlighting "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"

git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install

git clone https://github.com/spaceship-prompt/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1

ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
