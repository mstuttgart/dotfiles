#!/usr/bin/fish

# change to home folder
cd

# Make a git add
dot add --all

# Make a backup commit
dot commit -m "Daily backup: `date`"

# make a push
dot up
