local status, packer = pcall(require, 'packer')

-- check packer is installed
if (not status) then
  print('Packer is not installed')
  return
end

return packer.startup(function()

  -- packer
  use { 'wbthomason/packer.nvim' }

  -- show git change (change, delete, add) signs in vim sign column
  use { 'lewis6991/gitsigns.nvim' }

  -- better visual guide
  use { 'lukas-reineke/indent-blankline.nvim' }

  -- nvim-lsp configuration
  use { 'neovim/nvim-lspconfig' }

  -- comment code
  use {
      'numToStr/Comment.nvim',
      config = function()
          require('Comment').setup()
      end
  }
  -- show and trim trailing whitespaces
  use {
    "mcauley-penney/tidy.nvim",
    config = function()
      require('tidy').setup()
    end
  }

  -- highlight for color code
  use {
    'norcalli/nvim-colorizer.lua',
    config = function()
      require('colorizer').setup()
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
  }

  -- tag bar
  -- use { 'stevearc/aerial.nvim' }
  use { 'majutsushi/tagbar' }

  -- themes
  use { 'Shatur/neovim-ayu' }
  use { 'neanias/everforest-nvim' }

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
    run = ':TSUpdate',
   })

   -- create annotations for multiple linguages
   use {
    'danymat/neogen',
    requires = { "nvim-treesitter/nvim-treesitter" },
    tag = "*",
   }

  -- file explorer
  use {
    'nvim-tree/nvim-tree.lua',
    requires = { 'nvim-tree/nvim-web-devicons' },
  }

  -- markdown preview :MarkdownPreviewToggle
  use({
    "iamcco/markdown-preview.nvim",
    run = function() vim.fn["mkdp#util#install"]() end,
  })

  -- surround chars
  use({
      "kylechui/nvim-surround",
      tag = "*", -- Use for stability; omit to use `main` branch for the latest features
      config = function()
          require("nvim-surround").setup()
      end
  })

end)
