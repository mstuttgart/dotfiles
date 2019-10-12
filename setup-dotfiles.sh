#!/bin/bash

source colors.sh

print "Create symlinks to dotfiles"
new_line

# .bash_aliases ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Create bash aliases to use aliases
if [ -f "$HOME/.bash_aliases" ]; then
    msg_update ".bash_aliases"
    rm ~/.bash_aliases
else
    msg_install ".bash_aliases"
fi

ln -sfv $(pwd)/.bash_aliases ~/.bash_aliases
check_return_code $? ".bash_aliases symlink"

# .bashrc ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Override .bashrc with my settings
if [ -f "$HOME/.bashrc" ]; then
    msg_update ".bashrc"
    rm ~/.bashrc
else
    msg_install ".bashrc"
fi

ln -sfv $(pwd)/.bashrc ~/.bashrc
check_return_code $? ".bashrc symlink"

# .gitconfig ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Override gitconfig file
if [ -f "$HOME/.gitconfig" ]; then
    msg_update ".gitconfig"
    rm ~/.gitconfig
else
    msg_install ".gitconfig"
fi

ln -sfv $(pwd)/.gitconfig ~/.gitconfig
check_return_code $? ".gitconfig symlink"
