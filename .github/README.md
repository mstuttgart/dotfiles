<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="dotfiles.png" width="80%">
  </a>
</p>

## About

This repository serves as my way to help me setup and maintain my Linux Mint.

![Screenshot from 2024-11-03 14-31-57](https://github.com/user-attachments/assets/98905a99-dd9e-42ec-99a5-9ae0f5ecbdb4)

- OS: [Linux Mint 22 Cinnamon](https://linuxmint.com/)
- Shell: [zsh](https://github.com/zsh-users/zsh)
  - [pure](https://github.com/sindresorhus/pure)                                                   : Minimalistic, powerful and extremely customizable Zsh prompt
  - [zplug](https://github.com/zplug/zplug)                                                        : A next-generation plugin manager for zsh
  - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)                : Fish shell like syntax highlighting for Zsh.
  - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)                        : Fish-like autosuggestions for zsh
  - [zsh-z](https://github.com/agkozak/zsh-z)                                                      : A native Zsh port of z.sh with added features.
  - [zsh-autopair](https://github.com/hlissner/zsh-autopair)                                       : Auto-close and delete matching delimiters in zsh
  - [asdf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/asdf)                            : *Oh-My-Zsh* asdf plugin
  - [fzf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/fzf)                              : *Oh-My-Zsh* fzf plugin
  - [virtualenvwrapper](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/virtualenvwrapper)  : *Oh-My-Zsh* python virtualenvwrapper plugin
- Terminal: [alacritty](https://github.com/alacritty/alacritty)
  - [tig](https://github.com/jonas/tig)             : Text-mode interface for git
  - [bat](https://github.com/sharkdp/bat)           : A cat(1) clone with wings
  - [fzf](https://github.com/junegunn/fzf)          : A command-line fuzzy finder
  - [eza](https://github.com/eza-community/eza)     : A modern replacement for ‘ls’
  - [btop](https://github.com/aristocratos/btop)    : A monitor of resources
- Editor: [neovim](https://neovim.io/) -- check my configuration [here](https://github.com/mstuttgart/nvim)

## Setup

> [!CAUTION]
> Settings applied by this repository are very personal, and definitely not suite everyones needs. Don’t blindly use my settings unless you know what that entails. Use at your own risk!

My dotfiles is managed by [yadm](https://yadm.io), a dotfiles manager. This makes it simple to set up a new computer and keep updates my config files. I order to set up a new system with these dotfiles, do the following:

```sh
sudo apt install yadm git -y
```

To others systems install instructions, see [here](https://yadm.io/docs/install).

### Get the dots

Use `yadm` to clone this repo and set up your enviromnent.

```sh
yadm clone git@github.com:mstuttgart/dotfiles.git --no-bootstrap
```

The `clone` and `pull` command may result in warnings because of pre-existing dotfiles. Overwrite the existing files with commands below.

```sh
yadm reset --hard origin/linux-mint-22

# download nvim
git clone git@github.com:mstuttgart/nvim.git .config/nvim
```

Execute the follow command to install all dependencies and apps:

```sh
yadm bootstrap
```
