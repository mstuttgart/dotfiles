<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="https://user-images.githubusercontent.com/8174740/236652567-5927a005-e18b-4037-b92a-8779cdf2c970.png" width="60%">
  </a>
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#install">Install</a> |
  <a href="#credits">Credits</a>
</p>

## About

![2023-05-06_10-41](https://user-images.githubusercontent.com/8174740/236627842-bd9fea77-8537-408e-ac8c-0b2db0a24c96.png)

This repository serves as my way to help me setup and maintain my Ubuntu (version 22.04 LTS).

> **Warning**: Settings applied by this repository are very personal, and definitely not suite everyones needs. Don’t blindly use my settings unless you know what that entails. Use at your own risk!

Here are some details about my setup:

- **WM**                           : [i3](https://github.com/i3/i3)
- **Shell**                        : [fish](https://fishshell.com/) with [tide](https://github.com/IlanCosman/tide) theme plugin!
- **Terminal**                     : [kitty](https://github.com/kovidgoyal/kitty)
- **Panel**                        : [polybar](https://github.com/polybar/polybar) using [nerd fonts](https://github.com/ryanoasis/nerd-fonts)!
- **Compositor**                   : [picom](https://github.com/chjj/compton)
- **Notify Daemon**                : [dunst](https://wiki.archlinux.org/index.php/Dunst)
- **Application Launcher**         : [rofi](https://github.com/davatorium/rofi) apps menu and windows!
- **File Manager**                 : [ranger](https://github.com/ranger/ranger)
- **Wallpaper Manager**            : [nitrogen](https://github.com/l3ib/nitrogen)
- **Editor**                       : [neovim](https://neovim.io/)

## Install

I use the `bare` repo git to store my dotfiles. More about [here](https://www.atlassian.com/git/tutorials/dotfiles).

Clone this repo:

```sh
# create alias
alias dgit='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# clone base repo
git clone --bare git@github.com:mstuttgart/dotfiles.git $HOME/.dotfiles

# disable untracked files
dgit config --local status.showUntrackedFiles no

# checkout
dgit checkout
```

## Credits

Copyright (C) 2019-2023 by Michell Stuttgart
