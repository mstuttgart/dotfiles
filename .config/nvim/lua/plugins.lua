
return require('packer').startup(function()

  -- packer
  use 'wbthomason/packer.nvim'

  -- initial screen
  use {
    'goolord/alpha-nvim',
    requires = { 'nvim-tree/nvim-web-devicons' },
    config = [[require('config.alpha')]],
  }

  -- show git change (change, delete, add) signs in vim sign column
  use {
    'lewis6991/gitsigns.nvim',
    config = [[require('config.gitsigns')]],
  }

  -- generate links to git web frontend hosts
  use {
    'ruifm/gitlinker.nvim',
    requires = 'nvim-lua/plenary.nvim',
    event = 'User InGitRepo',
    config = [[require('config.git-linker')]],
  }

  -- git fugitive in lua. Use git inside vim
  use {
    'dinhhuy258/git.nvim',
    config = function()
      require('git').setup({
        -- Default target branch when create a pull request
        target_branch = "develop",
      })
    end
  }

  -- better visual guide
  use {
    "lukas-reineke/indent-blankline.nvim",
    event = "VimEnter",
    config = [[require('config.indent-blankline')]],
  }

  -- nvim-lsp configuration
  use {
    "neovim/nvim-lspconfig",
    config = [[require('config.lsp')]],
  }

  -- comment code
  -- use 'scrooloose/nerdcommenter'
  use { "tpope/vim-commentary", event = "VimEnter" }

  -- Python indent (follows the PEP8 style)
  use { "Vimjas/vim-python-pep8-indent", ft = { "python" } }

  -- Highlight URLs inside vim
  use { "itchyny/vim-highlighturl", event = "VimEnter" }

  -- show and trim trailing whitespaces
  use {
    "mcauley-penney/tidy.nvim",
    config = function()
      require('tidy').setup()
    end
  }

  -- lua support
  use { "ii14/emmylua-nvim", ft = "lua" }

  -- highlight for color code
  use {
    'brenoprata10/nvim-highlight-colors',
    config = function()
      require('nvim-highlight-colors').setup()
    end
  }

  -- format code
  use { 'sbdchd/neoformat', cmd = {'Neoformat'}}

  -- auto close chars like '(', '{', '[' and ""
  -- use {
  --   'm4xshen/autoclose.nvim',
  --   config = function()
  --     require('autoclose').setup()
  --   end
  -- }

  use {
    'windwp/nvim-autopairs',
    config = function()
      require('nvim-autopairs').setup()
    end
  }

  -- general language snippets
  use { "rafamadriz/friendly-snippets" }

  -- telescope
  use {
    'nvim-telescope/telescope.nvim',
    requires = { 'nvim-lua/plenary.nvim'},
    config = function()
      require('telescope').setup()
    end
  }

  -- telescope fzf
  use {
    'nvim-telescope/telescope-fzf-native.nvim',
    run = 'make',
    requires = { 'nvim-telescope/telescope.nvim'},
    config = function()
      require('telescope').load_extension('fzf')
    end
    }

  -- tag bar
  use { 'majutsushi/tagbar' }

  -- themes
  use { 'morhetz/gruvbox', opt = true }
  use { 'nordtheme/vim', opt = true }
  use { 'Shatur/neovim-ayu' }
  use { 'neanias/everforest-nvim'}

  -- lualine status bar
  use {
    'nvim-lualine/lualine.nvim',
    requires = { 'nvim-tree/nvim-web-devicons' },
    config = function()
      require('lualine').setup()
    end
  }

  -- syntax support
  use({
     'nvim-treesitter/nvim-treesitter',
     event = 'BufEnter',
     config = [[require('config.treesitter')]],
     run = ':TSUpdate',
   })

   -- create annotations for multiple linguages
   use {
       'danymat/neogen',
       event = 'BufEnter',
       requires = "nvim-treesitter/nvim-treesitter",
       tag = "*",
   }
  -- use {
  --   'pixelneo/vim-python-docstring',
  --   event = 'BufEnter',
  -- }

  -- file explorer
  use {
    'nvim-tree/nvim-tree.lua',
    requires = { 'nvim-tree/nvim-web-devicons' },
    config = [[require('config.nvim-tree')]],
  }

  -- markdown preview :MarkdownPreviewToggle
  use({
      "iamcco/markdown-preview.nvim",
      run = function() vim.fn["mkdp#util#install"]() end,
  })

end)
