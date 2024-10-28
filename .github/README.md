<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="dotfiles.png" width="80%">
  </a>
</p>

<pre align="center">
<a href="#about">ABOUT</a> • <a href="#setup">SETUP</a> • <a href="#keybinds">KEYBINDS</a> 
</pre>


## About

This repository serves as my way to help me setup and maintain my ArchLinux.

<!-- <img src="https://github.com/mstuttgart/dotfiles/assets/8174740/e0205c3a-57db-463d-84e5-84dc4d50dfcd" alt="img" align="right" width="500px"> -->

![2024-05-17_20-53_1 Everforest Dark](https://github.com/mstuttgart/dotfiles/assets/8174740/e0205c3a-57db-463d-84e5-84dc4d50dfcd)

- OS: [Arch Linux]()
- Window Manager: [i3wm](https://github.com/i3/i3)
- Shell: [zsh](https://github.com/zsh-users/zsh)
  - [spaceship-prompt](https://github.com/spaceship-prompt/spaceship-prompt)                       : Minimalistic, powerful and extremely customizable Zsh prompt
  - [zplug](https://github.com/zplug/zplug)                                                        : A next-generation plugin manager for zsh
  - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)                : Fish shell like syntax highlighting for Zsh.
  - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)                        : Fish-like autosuggestions for zsh
  - [zsh-z](https://github.com/agkozak/zsh-z) : Jump quickly to directories that you have visited "frecently." A native Zsh port of z.sh with added features.
  - [zsh-autopair](https://github.com/hlissner/zsh-autopair)                                       : Auto-close and delete matching delimiters in zsh
  - [git](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git)                              : *Oh My Zsh* git plugin
  - [asdf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/asdf)                            : *Oh-My-Zsh* asdf plugin
  - [fzf](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/fzf)                              : *Oh-My-Zsh* fzf plugin
  - [virtualenvwrapper](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/virtualenvwrapper)  : *Oh-My-Zsh* python virtualenvwrapper plugin
- Terminal: [alacritty](https://github.com/alacritty/alacritty)
  - [tig](https://github.com/jonas/tig)             : Text-mode interface for git
  - [bat](https://github.com/sharkdp/bat)           : A cat(1) clone with wings
  - [fzf](https://github.com/junegunn/fzf)          : A command-line fuzzy finder
  - [eza](https://github.com/eza-community/eza)     : A modern replacement for ‘ls’
  - [btop](https://github.com/aristocratos/btop)    : A monitor of resources
- Bar: [polybar](https://github.com/polybar/polybar) using [nerd fonts](https://github.com/ryanoasis/nerd-fonts)!
  - Everforest theme (dark/light)
  - Gruvbox theme (dark)
  - Gruvbox Material theme (dark)
  - Ayu theme (dark, light and mirage)
  - Nord theme (dark)
  - TokyoNight theme (dark)
- Compositor: [picom](https://github.com/yshui/picom)
- Notify Daemon: [dunst](https://wiki.archlinux.org/index.php/Dunst)
- Application Launcher: [rofi](https://github.com/davatorium/rofi)
- Editor: [neovim](https://neovim.io/) -- check my configuration [here](https://github.com/mstuttgart/nvim)
- File Manager: [thunar](https://docs.xfce.org/xfce/thunar/start)

## Setup

> [!CAUTION]
> Settings applied by this repository are very personal, and definitely not suite everyones needs. Don’t blindly use my settings unless you know what that entails. Use at your own risk!

My dotfiles is managed by [yadm](https://yadm.io), a dotfiles manager. This makes it simple to set up a new computer and keep updates my config files. I order to set up a new system with these dotfiles, do the following:

```sh
sudo pacman -S yadm
```

To others systems install instructions, see [here](https://yadm.io/docs/install).

### Get the dots

Use `yadm` to clone this repo and set up your enviromnent.

```sh
yadm clone --recursive https://github.com/mstuttgart/dotfiles.git --no-bootstrap
```

The `clone` and `pull` command may result in warnings because of pre-existing dotfiles. Overwrite the existing files with commands below.

```sh
yadm reset --hard origin/main

# download nvim
yadm submodule update --recursive --init

# update repo url
yadm remote set-url origin "git@github.com:MyUser/dotfiles.git"
```

Execute the follow command to install all dependencies and apps:

```sh
yadm bootstrap
```

## Keybinds

I use <kbd>super</kbd> AKA Windows key as my main modifier.

#### Keyboard
| Keybind | Action |
| --- | --- |
| <kbd>super + enter</kbd> | Spawn terminal |
| <kbd>super + b</kbd> | Spawn browser |
| <kbd>super + shift + b</kbd> | Launch browser in incognito mode |
| <kbd>super + f</kbd> | Launch file manager |
| <kbd>super + t</kbd> | Launch msteams |
| <kbd>super + d</kbd> | Launch rofi |
| <kbd>super + q</kbd> | Kill application |
| <kbd>Prtsc</kbd> | Launch flameshot (screenshot) |
| <kbd>super + space</kbd> | Toggle floating client |
| <kbd>super + shift + space</kbd> | Focus floating client |
| <kbd>super + [1-0]</kbd> | Change workspace |
| <kbd>super + tab</kbd> | Move to next workspace |
| <kbd>super + shift + tab</kbd> | Move to prevous workspace |
| <kbd>super + shift + [1-0]</kbd> | Move window to workspace |
| <kbd>super + w</kbd> | Stacking layout |
| <kbd>super + s</kbd> | Tabbed layout |
| <kbd>super + e</kbd> | Stacking / Tabbed / toogle layout split |
| <kbd>super + shift + [hjkl]</kbd> | Move focus |
| <kbd>super + shift + [hjkl]</kbd> | Move focused window |
| <kbd>super + F2 </kbd> |Enter Resize mode |
| <kbd> (in resize mode) [arrow keys]</kbd> | Resize client |
| <kbd> (in resize mode) ESC|RETURN</kbd> | Back to Normal mode |
| <kbd>super + F1</kbd> | Reload i3wm config |
| <kbd>super + F5</kbd> | Reload i3wm |

