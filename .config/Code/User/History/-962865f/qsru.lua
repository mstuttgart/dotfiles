-- configure 'plug-n-play' plugins

return {

  -- colorscheme
  {
    'Shatur/neovim-ayu',
    lazy = true
  },

  {
    'navarasu/onedark.nvim',
    lazy = true
  },

  {
    'shaunsingh/nord.nvim',
    lazy = true
  },

  {
    'neanias/everforest-nvim',
    lazy = false,
    priority = 1000,
    config = function()
      require "plugins.configs.everforest"
    end,
  },

  -- highlight for HEX color code
  {
    'norcalli/nvim-colorizer.lua',
    lazy = true,
    config = function()
      require('colorizer').setup(nil, { css = true })
    end,
  },

  -- icons, for UI related plugins
  {
    "nvim-tree/nvim-web-devicons",
    config = function()
      require("nvim-web-devicons").setup()
    end,
  },


  -- Useful plugin to show you pending keybinds.
  {
    'folke/which-key.nvim',
    opts = {},
    lazy = true,
  },

  -- statusline
  {
    'nvim-lualine/lualine.nvim',
    dependencies = {
        'nvim-tree/nvim-tree.lua',
        },
    event = 'VeryLazy',
    config = function()
      require "plugins.configs.lua/"

    end,
  },

  -- auto close chars like '(', '{', '[' and ''
  {
    'windwp/nvim-autopairs',
    lazy = true,
    config = true,
  },

  -- buffer + tab line
  {
    "akinsho/bufferline.nvim",
    event = "BufReadPre",
    dependencies = {
      { 'echasnovski/mini.bufremove', version = '*' },
    },
    keys = {
      { '<leader>bQ', '<Cmd>BufferLineGroupClose ungrouped<CR>', desc = 'Delete all buffers' },
      { '<leader>bQ', '<Cmd>BufferLineCycleNext<CR>', desc = 'Delete all buffers' },
      { '<leader>bQ', '<Cmd>BufferLineGroupClose ungrouped<CR>', desc = 'Delete all buffers' },
      { '<leader>bQ', '<Cmd>BufferLineGroupClose ungrouped<CR>', desc = 'Delete all buffers' },

    },
    config = function()
      require "plugins.configs.bufferline"
    end,
  },

  -- git status on signcolumn etc
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
      require "plugins.configs.gitsigns"
    end,
  },

  -- indent lines
  {
    "lukas-reineke/indent-blankline.nvim",
    version = "2.20.7",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
      require "plugins.configs.blankline"
    end,
  },

  -- syntax highlighting
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      require "plugins.configs.treesitter"
    end,
  },

  -- file tree
  {
    "nvim-tree/nvim-tree.lua",
    cmd = { "NvimTreeToggle", "NvimTreeFocus" },
    config = function()
      require "plugins.configs.nvim_tree"
    end,
    keys = {
      { '<leader>tt', '<cmd>NvimTreeToggle<cr>',   desc = '[T]oggle  [T]ree' },
      { '<leader>tf', '<cmd>NvimTreeFindFile<cr>', desc = '[T]ree open with current [F]ile' },
      { '<leader>tr', '<cmd>NvimTreeRefresh<cr>',  desc = '[T]ree [R]efresh' },
    },
    init = function()
      -- change background color of tree
      vim.cmd('autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE')
      vim.cmd('autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE')
    end,
  },

  -- { lazy = true, "nvim-lua/plenary.nvim" },



  -- -- we use cmp plugin only when in insert mode
  -- -- so lets lazyload it at InsertEnter event, to know all the events check h-events
  -- -- completion , now all of these plugins are dependent on cmp, we load them after cmp
  -- {
  --   "hrsh7th/nvim-cmp",
  --   event = "InsertEnter",
  --   dependencies = {
  --     -- cmp sources
  --     "hrsh7th/cmp-buffer",
  --     "hrsh7th/cmp-path",
  --     "hrsh7th/cmp-nvim-lsp",
  --     "saadparwaiz1/cmp_luasnip",
  --     "hrsh7th/cmp-nvim-lua",

  --     -- snippets
  --     --list of default snippets
  --     "rafamadriz/friendly-snippets",

  --     -- snippets engine
  --     {
  --       "L3MON4D3/LuaSnip",
  --       config = function()
  --         require("luasnip.loaders.from_vscode").lazy_load()
  --       end,
  --     },

  --     -- autopairs , autocompletes ()[] etc
  --     {
  --       "windwp/nvim-autopairs",
  --       config = function()
  --         require("nvim-autopairs").setup()

  --         --  cmp integration
  --         local cmp_autopairs = require "nvim-autopairs.completion.cmp"
  --         local cmp = require "cmp"
  --         cmp.event:on("confirm_done", cmp_autopairs.on_confirm_done())
  --       end,
  --     },
  --   },
  --   config = function()
  --     require "plugins.configs.cmp"
  --   end,
  -- },

  -- {
  --   "williamboman/mason.nvim",
  --   build = ":MasonUpdate",
  --   cmd = { "Mason", "MasonInstall" },
  --   config = function()
  --     require("mason").setup()
  --   end,
  -- },

  -- lsp
  -- {
  --   "neovim/nvim-lspconfig",
  --   event = { "BufReadPre", "BufNewFile" },
  --   config = function()
  --     require "plugins.configs.lspconfig"
  --   end,
  -- },

  -- formatting , linting
  -- {
  --   "stevearc/conform.nvim",
  --   lazy = true,
  --   config = function()
  --     require "plugins.configs.conform"
  --   end,
  -- },



  -- files finder etc
  -- {
  --   "nvim-telescope/telescope.nvim",
  --   cmd = "Telescope",
  --   config = function()
  --     require "plugins.configs.telescope"
  --   end,
  -- },



  -- comment plugin
  {
    "numToStr/Comment.nvim",
    lazy = true,
    config = function()
      require("Comment").setup()
    end,
  },
}

-- require("lazy").setup(plugins, require "plugins.configs.lazy")
