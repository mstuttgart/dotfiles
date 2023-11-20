#!/usr/bin/bash

# change to home folder
cd

# Make a git add
yadm add .

# Make a backup commit
yadm commit -m "Daily backup: `date`"

# make a push
yadm up
