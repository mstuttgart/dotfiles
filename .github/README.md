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

![2023-05-06_10-41](screenshot.png)

This repository serves as my way to help me setup and maintain my Ubuntu (version 22.04 LTS).

Here are some details about my setup:

- **Linux Distribution**           : [Linux Mint](https://www.linuxmint.com/)
- **Window Manager**               : [i3](https://github.com/i3/i3)
- **Shell**                        : [fish](https://fishshell.com/) with [tide](https://github.com/IlanCosman/tide) theme plugin!
- **Terminal**                     : [kitty](https://github.com/kovidgoyal/kitty)
- **Bar**                        : [polybar](https://github.com/polybar/polybar) using [nerd fonts](https://github.com/ryanoasis/nerd-fonts)!
- **Compositor**                   : [compton](https://github.com/chjj/compton)
- **Notify Daemon**                : [dunst](https://wiki.archlinux.org/index.php/Dunst)
- **Application Launcher**         : [rofi](https://github.com/davatorium/rofi)
- **File Manager**                 : [ranger](https://github.com/ranger/ranger)
- **Wallpaper Manager**            : [nitrogen](https://github.com/l3ib/nitrogen)
- **Editor**                       : [neovim](https://neovim.io/)
- **CLI System Information**       : [neofetch](https://github.com/dylanaraps/neofetch)

### Neovim Setup

Requires [Neovim](https://neovim.io/) (>= 0.8)

- [folke/lazy.nvim](https://github.com/folke/lazy.nvim) - A modern plugin manager for Neovim
- [utilyre/barbecue.nvim](https://github.com/utilyre/barbecue.nvim) - A VS Code like winbar for Neovim
- [akinsho/bufferline.nvim](https://github.com/akinsho/bufferline.nvim) -  A snazzy bufferline for Neovim 
- [hrsh7th/cmp-buffer](https://github.com/hrsh7th/cmp-buffer) - nvim-cmp source for buffer words
- [hrsh7th/cmp-cmdline](https://github.com/hrsh7th/cmp-cmdline) - nvim-cmp source for vim's cmdline 
- [hrsh7th/cmp-nvim-lsp](https://github.com/hrsh7th/cmp-nvim-lsp) - nvim-cmp source for neovim's built-in LSP
- [hrsh7th/cmp-nvim-lua](https://github.com/hrsh7th/cmp-nvim-lua) - nvim-cmp source for nvim lua
- [hrsh7th/cmp-path](https://github.com/hrsh7th/cmp-path) - nvim-cmp source for path 
- [saadparwaiz1/cmp_luasnip](https://github.com/saadparwaiz1/cmp_luasnip) - luasnip completion source for nvim-cmp
- [stevearc/dressing.nvim](https://github.com/stevearc/dressing.nvim) - Neovim plugin to improve the default vim.ui interfaces 
- [neanias/everforest-nvim](https://github.com/neanias/everforest-nvim) - A Lua port of the Everforest colour scheme
- [j-hui/fidget.nvim](https://github.com/j-hui/fidget.nvim) - Standalone UI for nvim-lsp progress 
- [rafamadriz/friendly-snippets](https://github.com/rafamadriz/friendly-snippets) - Set of preconfigured snippets for different languages. 
- [lewis6991/gitsigns.nvim](https://github.com/lewis6991/gitsigns.nvim) - Git integration for buffers
- [lukas-reineke/indent-blankline.nvim](https://github.com/lukas-reineke/indent-blankline.nvim) - Indent guides for Neovim
- [onsails/lspkind.nvim](https://github.com/onsails/lspkind.nvim) - vscode-like pictograms for neovim lsp completion items 
- [nvim-lualine/lualine.nvim](https://github.com/nvim-lualine/lualine.nvim) - A blazing fast and easy to configure Neovim statusline written in Lua
- [iamcco/markdown-preview.nvim](https://github.com/iamcco/markdown-preview.nvim) - Markdown live preview
- [williamboman/mason-lspconfig.nvim](https://github.com/williamboman/mason-lspconfig.nvim) - Extension to mason.nvim that makes it easier to use lspconfig
- [williamboman/mason.nvim](https://github.com/williamboman/mason.nvim) - Portable package manager for Neovim that runs everywhere Neovim runs.
- [echasnovski/mini.bufremove](https://github.com/echasnovski/mini.bufremove) - Neovim Lua plugin to remove buffers. Part of 'mini.nvim' library
- [echasnovski/mini.comment](https://github.com/echasnovski/mini.comment) - Neovim Lua plugin for fast and familiar per-line commenting. Part of 'mini.nvim' library
- [echasnovski/mini.starter](https://github.com/echasnovski/mini.starter) - Neovim Lua plugin with fast and flexible start screen. Part of 'mini.nvim' library.
- [echasnovski/mini.surround](https://github.com/echasnovski/mini.surround) - Neovim Lua plugin with fast and feature-rich surround actions. Part of 'mini.nvim' library. 
- [folke/neodev.nvim](https://github.com/folke/neodev.nvim) - Neovim setup for init.lua and plugin development with full signature help, docs and completion for the nvim lua API.
- [danymat/neogen](https://github.com/danymat/neogen) - A better annotation generator. Supports multiple languages and annotation conventions
- [folke/noice.nvim](https://github.com/folke/noice.nvim) - Highly experimental plugin that completely replaces the UI for messages, cmdline and the popupmenu. 
- [MunifTanjim/nui.nvim](https://github.com/MunifTanjim/nui.nvim) - UI Component Library for Neovim.
- [jose-elias-alvarez/null-ls.nvim](https://github.com/jose-elias-alvarez/null-ls.nvim) - Use Neovim as a language server to inject LSP diagnostics, code actions, and more via Lua.
- [windwp/nvim-autopairs](https://github.com/windwp/nvim-autopairs) - autopairs for neovim written by lua
- [hrsh7th/nvim-cmp](https://github.com/hrsh7th/nvim-cmp) - A completion engine plugin for neovim written in Lua
- [norcalli/nvim-colorizer.lua](https://github.com/norcalli/nvim-colorizer.lua) - A high-performance color highlighter
- [neovim/nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) - A collection of configurations for Neovim's built-in LSP
- [SmiteshP/nvim-navic](https://github.com/SmiteshP/nvim-navic) - Simple winbar/statusline plugin that shows your current code context
- [rcarriga/nvim-notify](https://github.com/rcarriga/nvim-notify) - https://github.com/rcarriga/nvim-notify
- [nvim-tree/nvim-tree.lua](https://github.com/nvim-tree/nvim-tree.lua)
- [nvim-treesitter/nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter) - [Treesitter](https://github.com/tree-sitter/tree-sitter) configurations and abstraction layer for Neovim
- [windwp/nvim-ts-autotag](https://github.com/windwp/nvim-ts-autotag) - Use treesitter to auto close and auto rename html tag
- [kyazdani42/nvim-web-devicons](https://github.com/kyazdani42/nvim-web-devicons) - Lua `fork` of vim-web-devicons for neovim
- [folke/persistence.nvim](https://github.com/folke/persistence.nvim) - Simple session management for Neovim 
- [nvim-lua/plenary.nvim](https://github.com/nvim-lua/plenary.nvim) - plenary: full; complete; entire; absolute; unqualified. All the lua functions I don't want to write twice.
- [mechatroner/rainbow_csv](https://github.com/mechatroner/rainbow_csv) - Highlight columns in CSV and TSV files and run queries in SQL-like language 
- [simrat39/symbols-outline.nvim](https://github.com/simrat39/symbols-outline.nvim) - A tree like view for symbols in Neovim using the Language Server Protocol
- [nvim-telescope/telescope.nvim](https://github.com/nvim-telescope/telescope.nvim) - A highly extendable fuzzy finder over lists
- [nvim-telescope/telescope-fzf-native.vim](https://github.com/nvim-telescope/telescope-fzf-native.nvim) -  FZF sorter for telescope written in c
- [folke/trouble.nvim](https://github.com/folke/trouble.nvim) - A pretty diagnostics, references, telescope results, quickfix and location list to help you solve all the trouble your code is causing. 
- [RRethy/vim-illuminate](https://github.com/RRethy/vim-illuminate) - (Neo)Vim plugin for automatically highlighting other uses of the word under the cursor using either LSP, Tree-sitter, or regex matching. 
- [folke/which-key.nvim](https://github.com/folke/which-key.nvim) - WhichKey is a lua plugin that displays a popup with possible keybindings of the command you started typing. 
- [L3MON4D3/LuaSnip](https://github.com/L3MON4D3/LuaSnip) - Snippet Engine for Neovim written in Lua

### Shell Setup

- [Fish shell](https://fishshell.com/)
- [Fisher](https://github.com/jorgebucaran/fisher) - Plugin manager
    - [z](https://github.com/jethrokuan/z) - Directory jumping
    - [autopair](https://github.com/jorgebucaran/autopair.fish) -  Auto-complete matching pairs in the Fish command line
    - [fzf](https://github.com/PatrickF1/fzf.fish) - Fzf plugin for Fish
- [Starship](https://starship.rs/) - Shell theme. The minimal, blazing-fast, and infinitely customizable prompt for any shell!
- [exa](https://the.exa.website/) - `ls` replacement
- [bat](https://github.com/sharkdp/bat) - A `cat`(1) clone with wings
- [btop](https://github.com/aristocratos/btop) - A monitor of resources
- [tig](https://github.com/jonas/tig) - Text-mode interface for git
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) - I use JetBrains and Sauce Code Pro (icons of Polybar)

## Install

> **Warning**: Settings applied by this repository are very personal, and definitely not suite everyones needs. Don’t blindly use my settings unless you know what that entails. Use at your own risk!

My dotfiles is managed by [yadm](https://yadm.io), a dotfiles manager. This makes it simple to set up a new computer and keep updates my config files. I order to set up a new system with these dotfiles, do the following:

### Debian/Ubuntu

```sh
$ apt install yadm
```

To others systems install instructions, see [here](https://yadm.io/docs/install).

### Set up

Use `yadm` to clone this repo and set up your enviromnent.

```sh
yadm clone git@github.com:mstuttgart/dotfiles.git
```

The `clone` and `pull` command may result in warnings because of pre-existing dotfiles. Overwrite the existing files with commands below.

```sh
yadm fetch --all
yadm reset --hard origin/main
```

## Credits

Copyright (C) 2019-2023 by Michell Stuttgart
