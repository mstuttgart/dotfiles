#!/usr/bin/bash
#
notify-send "📦 Dotfiles Sync" "Starting dotfiles repository sync..."

# change to home folder
cd "$HOME" || exit

# git stages modification and deletions, without new files 
yadm add -u

# Make a backup commit
yadm commit -m "Daily backup: $(date)"

# Get remote updates
yadm pull --rebase origin main

# make a push
yadm push origin main

notify-send "📦 Dotfiles Sync" "Dotfiles sync complete."
