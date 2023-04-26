
return require('packer').startup(function()

  -- packer
  use 'wbthomason/packer.nvim'

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
  use { "tpope/vim-commentary", event = "VimEnter" }

  -- show and trim trailing whitespaces
  use {
    "mcauley-penney/tidy.nvim",
    config = function()
      require('tidy').setup()
    end
  }

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
  -- use { 'nordtheme/vim' }
  use { 'shaunsingh/nord.nvim' }
  use { 'Shatur/neovim-ayu' }

  use {
    'neanias/everforest-nvim',
    config = function()
      require("everforest").setup({
        -- Controls the "hardness" of the background. Options are "soft", "medium" or "hard".
        -- Default is "medium".
        background = "medium",
        -- How much of the background should be transparent. Options are 0, 1 or 2.
        -- Default is 0.
        --
        -- 2 will have more UI components be transparent (e.g. status line
        -- background).
        transparent_background_level = 1,
        -- Whether italics should be used for keywords, builtin types and more.
        italics = true,
        -- Disable italic fonts for comments. Comments are in italics by default, set
        -- this to `true` to make them _not_ italic!
        disable_italic_comments = false,
      })
    end
  }

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
      config = function()
        require('neogen').setup()
      end,
      requires = { "nvim-treesitter/nvim-treesitter" },
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

  -- terminal
  use {
      's1n7ax/nvim-terminal',
      config = function()
          vim.o.hidden = true
          require('nvim-terminal').setup()
      end,
  }
end)
