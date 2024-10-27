#!/bin/bash

# turn on numlock
numlockx on

# caps lock works as escape
setxkbmap -layout pl -option caps:escape

# change keyboard layout to pt-BR
setxkbmap -model abnt2 -layout br

# exec i3
exec i3
