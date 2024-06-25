<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="dotfiles.png" width="80%">
  </a>
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#install">Install</a> |
  <a href="#credits">Credits</a>
</p>

## About

<!--![2023-12-27_15-21](https://github.com/mstuttgart/dotfiles/assets/8174740/63935f69-5774-4196-967a-9ef907790493) -->

![2024-05-17_20-53_1 Everforest Dark](https://github.com/mstuttgart/dotfiles/assets/8174740/e0205c3a-57db-463d-84e5-84dc4d50dfcd)
![2024-05-17_20-53 Everforest Light](https://github.com/mstuttgart/dotfiles/assets/8174740/7753990c-9c5d-4c80-8c68-6a07c5d74e0c)

This repository serves as my way to help me setup and maintain my Linux Mint 21 (or Ubuntu 22.04 LTS).

Here are some details about my setup:

- **Linux Distribution**           : [Linux Mint 21 - Xfce](https://www.linuxmint.com/)
- **Window Manager**               : [i3-gaps](https://github.com/Airblader/i3)
- **Shell**                        : [zsh](https://github.com/zsh-users/zsh)
  - [spaceship-prompt](https://github.com/spaceship-prompt/spaceship-prompt)                       : Minimalistic, powerful and extremely customizable Zsh prompt
  - [zplug](https://github.com/zplug/zplug)                                                        : A next-generation plugin manager for zsh
  - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)                : Fish shell like syntax highlighting for Zsh.
  - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)                        : Fish-like autosuggestions for zsh
  - [zsh-z](https://github.com/agkozak/zsh-z)                                                      : Jump quickly to directories that you have visited "frecently." A native Zsh port of z.sh with added features.
  - [zsh-autopair](https://github.com/hlissner/zsh-autopair)                                       : Auto-close and delete matching delimiters in zsh
  - [git](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git)                              : *Oh My Zsh* git plugin
  - [asdf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/asdf)                            : *Oh-My-Zsh* asdf plugin
  - [fzf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/fzf)                              : *Oh-My-Zsh* fzf plugin
  - [virtualenvwrapper](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/virtualenvwrapper)  : *Oh-My-Zsh* python virtualenvwrapper plugin
- **Terminal**                     : [alacritty](https://github.com/alacritty/alacritty)
  - [tig](https://github.com/jonas/tig)             : Text-mode interface for git
  - [bat](https://github.com/sharkdp/bat)           : A cat(1) clone with wings
  - [fzf](https://github.com/junegunn/fzf)          : A command-line fuzzy finder
  - [exa](https://github.com/ogham/exa)             : A modern replacement for ‘ls’
  - [btop](https://github.com/aristocratos/btop)    : A monitor of resources
- **Bar**                          : [polybar](https://github.com/polybar/polybar) using [nerd fonts](https://github.com/ryanoasis/nerd-fonts)!
  - Everforest theme (dark/light)
  - Gruvbox theme (dark)
  - Gruvbox Material theme (dark)
  - Ayu theme (dark, light and mirage)
  - Nord theme (dark)
  - TokyoNight theme (dark)
- **Compositor**                   : [compton](https://github.com/chjj/compton)
- **Notify Daemon**                : [dunst](https://wiki.archlinux.org/index.php/Dunst)
- **Application Launcher**         : [rofi](https://github.com/davatorium/rofi)
- **Wallpaper Manager**            : [nitrogen](https://github.com/l3ib/nitrogen)
- **Editor**                       : [neovim](https://neovim.io/) -- check my configuration [here](https://github.com/mstuttgart/nvim)
- **File Manager**                 : [ranger](https://github.com/ranger/ranger) | [thunar](https://docs.xfce.org/xfce/thunar/start)
- **CLI System Information**       : [neofetch](https://github.com/dylanaraps/neofetch)

## Install

> [!CAUTION]
> Settings applied by this repository are very personal, and definitely not suite everyones needs. Don’t blindly use my settings unless you know what that entails. Use at your own risk!

My dotfiles is managed by [yadm](https://yadm.io), a dotfiles manager. This makes it simple to set up a new computer and keep updates my config files. I order to set up a new system with these dotfiles, do the following:

### Debian/Ubuntu

```sh
sudo apt install yadm
```

To others systems install instructions, see [here](https://yadm.io/docs/install).

### Set up

Use `yadm` to clone this repo and set up your enviromnent.

```sh
yadm clone https://github.com/mstuttgart/dotfiles.git
```

The `clone` and `pull` command may result in warnings because of pre-existing dotfiles. Overwrite the existing files with commands below.

```sh
yadm fetch --all
yadm reset --hard origin/main
```

Execute the follow command to install all dependencies and apps:

```sh
yadm bootstrap
```

## Credits

Copyright (C) 2019-2024 by Michell Stuttgart
