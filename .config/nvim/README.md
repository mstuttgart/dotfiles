# dotfiles/.config/nvim

<a href="https://dotfyle.com/mstuttgart/dotfiles-config-nvim"><img src="https://dotfyle.com/mstuttgart/dotfiles-config-nvim/badges/plugins?style=for-the-badge" /></a>
<a href="https://dotfyle.com/mstuttgart/dotfiles-config-nvim"><img src="https://dotfyle.com/mstuttgart/dotfiles-config-nvim/badges/leaderkey?style=for-the-badge" /></a>
<a href="https://dotfyle.com/mstuttgart/dotfiles-config-nvim"><img src="https://dotfyle.com/mstuttgart/dotfiles-config-nvim/badges/plugin-manager?style=for-the-badge" /></a>

## Install Instructions

 > Install requires Neovim 0.9+. Always review the code before installing a configuration.

Clone the repository and install the plugins:

```sh
git clone git@github.com:mstuttgart/dotfiles ~/.config/mstuttgart/dotfiles
NVIM_APPNAME=mstuttgart/dotfiles/.config/nvim nvim --headless +"Lazy! sync" +qa
```

Open Neovim with this config:

```sh
NVIM_APPNAME=mstuttgart/dotfiles/.config/nvim nvim
```

## Plugins

### bars-and-lines

+ [utilyre/barbecue.nvim](https://dotfyle.com/plugins/utilyre/barbecue.nvim)
+ [SmiteshP/nvim-navic](https://dotfyle.com/plugins/SmiteshP/nvim-navic)
### colorscheme

+ [sainnhe/gruvbox-material](https://dotfyle.com/plugins/sainnhe/gruvbox-material)
+ [neanias/everforest-nvim](https://dotfyle.com/plugins/neanias/everforest-nvim)
+ [shaunsingh/nord.nvim](https://dotfyle.com/plugins/shaunsingh/nord.nvim)
+ [catppuccin/nvim](https://dotfyle.com/plugins/catppuccin/nvim)
### comment

+ [echasnovski/mini.comment](https://dotfyle.com/plugins/echasnovski/mini.comment)
+ [danymat/neogen](https://dotfyle.com/plugins/danymat/neogen)
### completion

+ [hrsh7th/nvim-cmp](https://dotfyle.com/plugins/hrsh7th/nvim-cmp)
### cursorline

+ [echasnovski/mini.cursorword](https://dotfyle.com/plugins/echasnovski/mini.cursorword)
### editing-support

+ [windwp/nvim-autopairs](https://dotfyle.com/plugins/windwp/nvim-autopairs)
### file-explorer

+ [nvim-tree/nvim-tree.lua](https://dotfyle.com/plugins/nvim-tree/nvim-tree.lua)
### formatting

+ [stevearc/conform.nvim](https://dotfyle.com/plugins/stevearc/conform.nvim)
### fuzzy-finder

+ [nvim-telescope/telescope.nvim](https://dotfyle.com/plugins/nvim-telescope/telescope.nvim)
### git

+ [lewis6991/gitsigns.nvim](https://dotfyle.com/plugins/lewis6991/gitsigns.nvim)
+ [kdheepak/lazygit.nvim](https://dotfyle.com/plugins/kdheepak/lazygit.nvim)
### icon

+ [nvim-tree/nvim-web-devicons](https://dotfyle.com/plugins/nvim-tree/nvim-web-devicons)
### indent

+ [echasnovski/mini.indentscope](https://dotfyle.com/plugins/echasnovski/mini.indentscope)
### keybinding

+ [folke/which-key.nvim](https://dotfyle.com/plugins/folke/which-key.nvim)
+ [max397574/better-escape.nvim](https://dotfyle.com/plugins/max397574/better-escape.nvim)
### lsp

+ [onsails/lspkind.nvim](https://dotfyle.com/plugins/onsails/lspkind.nvim)
+ [mfussenegger/nvim-lint](https://dotfyle.com/plugins/mfussenegger/nvim-lint)
+ [simrat39/symbols-outline.nvim](https://dotfyle.com/plugins/simrat39/symbols-outline.nvim)
+ [nvimtools/none-ls.nvim](https://dotfyle.com/plugins/nvimtools/none-ls.nvim)
+ [neovim/nvim-lspconfig](https://dotfyle.com/plugins/neovim/nvim-lspconfig)
### lsp-installer

+ [williamboman/mason.nvim](https://dotfyle.com/plugins/williamboman/mason.nvim)
### markdown-and-latex

+ [iamcco/markdown-preview.nvim](https://dotfyle.com/plugins/iamcco/markdown-preview.nvim)
### nvim-dev

+ [nvim-lua/plenary.nvim](https://dotfyle.com/plugins/nvim-lua/plenary.nvim)
+ [MunifTanjim/nui.nvim](https://dotfyle.com/plugins/MunifTanjim/nui.nvim)
### plugin-manager

+ [folke/lazy.nvim](https://dotfyle.com/plugins/folke/lazy.nvim)
### scrolling

+ [karb94/neoscroll.nvim](https://dotfyle.com/plugins/karb94/neoscroll.nvim)
### search

+ [nvim-pack/nvim-spectre](https://dotfyle.com/plugins/nvim-pack/nvim-spectre)
### session

+ [rmagatti/auto-session](https://dotfyle.com/plugins/rmagatti/auto-session)
### snippet

+ [L3MON4D3/LuaSnip](https://dotfyle.com/plugins/L3MON4D3/LuaSnip)
+ [rafamadriz/friendly-snippets](https://dotfyle.com/plugins/rafamadriz/friendly-snippets)
### split-and-window

+ [echasnovski/mini.bufremove](https://dotfyle.com/plugins/echasnovski/mini.bufremove)
### statusline

+ [nvim-lualine/lualine.nvim](https://dotfyle.com/plugins/nvim-lualine/lualine.nvim)
### syntax

+ [nvim-treesitter/nvim-treesitter](https://dotfyle.com/plugins/nvim-treesitter/nvim-treesitter)
+ [kylechui/nvim-surround](https://dotfyle.com/plugins/kylechui/nvim-surround)
+ [nvim-treesitter/nvim-treesitter-textobjects](https://dotfyle.com/plugins/nvim-treesitter/nvim-treesitter-textobjects)
### tabline

+ [akinsho/bufferline.nvim](https://dotfyle.com/plugins/akinsho/bufferline.nvim)
### utility

+ [folke/noice.nvim](https://dotfyle.com/plugins/folke/noice.nvim)
+ [stevearc/dressing.nvim](https://dotfyle.com/plugins/stevearc/dressing.nvim)
+ [rcarriga/nvim-notify](https://dotfyle.com/plugins/rcarriga/nvim-notify)
## Language Servers

+ ansiblels
+ bashls
+ cssls
+ html
+ lemminx
+ lua_ls
+ marksman
+ pyright
+ svelte
+ tsserver


 This readme was generated by [Dotfyle](https://dotfyle.com)
