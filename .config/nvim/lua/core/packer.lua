-- plugins setttings
local ensure_packer = function()
  local fn = vim.fn
  local install_path = fn.stdpath('data')..'/site/pack/packer/start/packer.nvim'
  if fn.empty(fn.glob(install_path)) > 0 then
    fn.system({'git', 'clone', '--depth', '1', 'git@github.com:wbthomason/packer.nvim.git', install_path})
    vim.cmd [[packadd packer.nvim]]
    return true
  end
  return false
end

local packer_bootstrap = ensure_packer()

return require('packer').startup(function()

  -- packer
  use { 'wbthomason/packer.nvim' }

  -- nvim-lsp configuration
  -- configure mason to install and manage LSP servers, linters and formatters
  use {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "neovim/nvim-lspconfig",
  }

  -- autocomplete
  use {
    'hrsh7th/nvim-cmp',
    'hrsh7th/cmp-nvim-lsp',
    'L3MON4D3/LuaSnip',
    'saadparwaiz1/cmp_luasnip',
  }

  -- show git change (change, delete, add) signs in vim sign column
  use { 'lewis6991/gitsigns.nvim' }

  -- better visual guide
  use { 'lukas-reineke/indent-blankline.nvim' }

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
  use { 'norcalli/nvim-colorizer.lua' }

  -- format code
  use { 'sbdchd/neoformat', cmd = {'Neoformat'}}

  -- auto close chars like '(', '{', '[' and ""
  use {
    'windwp/nvim-autopairs',
    config = function()
      require('nvim-autopairs').setup()
    end
  }

  -- telescope
  use {
    'nvim-telescope/telescope.nvim',
    requires = { 'nvim-lua/plenary.nvim'},
    config = function()
      require('telescope').setup()
    end
  }

  -- tag bar
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


  -- Automatically set up your configuration after cloning packer.nvim
  if packer_bootstrap then
    require('packer').sync()
  end

end)
