local overrides = require "custom.configs.overrides"

---@type NvPluginSpec[]
local plugins = {

  -- Override plugin definition options
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      -- format & linting
      {
        "jose-elias-alvarez/null-ls.nvim",
        config = function()
          require "custom.configs.null-ls"
        end,
      },
    },
    config = function()
      require "plugins.configs.lspconfig"
      require "custom.configs.lspconfig"
    end, -- Override to setup mason-lspconfig
  },

  -- override plugin configs
  {
    "williamboman/mason.nvim",
    opts = overrides.mason,
  },

  {
    "nvim-treesitter/nvim-treesitter",
    opts = overrides.treesitter,
  },

  {
    "nvim-tree/nvim-tree.lua",
    opts = overrides.nvimtree,
  },

  {
    "lewis6991/gitsigns.nvim",
    opts = overrides.gitsigns,
  },

  -- Install a plugin
  {
    "max397574/better-escape.nvim",
    event = "InsertEnter",
    config = function()
      require("better_escape").setup()
    end,
  },

  -- symbols panel
  {
    "simrat39/symbols-outline.nvim",
    lazy = true,
    cmd = "SymbolsOutline",
    keys = { { "<leader>cs", "<cmd>SymbolsOutline<cr>", desc = "Symbols Outline" } },
    config = function()
      require("symbols-outline").setup {
        vim.api.nvim_create_autocmd("BufEnter", {
          pattern = "*",
          command = "hi SymbolsOutlineConnector gui=none guifg=vim.g.foreground",
        }),
      }
    end,
  },

  -- auto close chars like '(', '{', '[' and ''
  {
    "windwp/nvim-autopairs",
    lazy = true,
    config = true,
  },

  -- navic complement to breadcumbs
  {
    "utilyre/barbecue.nvim",
    lazy = true,
    version = "*",
    dependencies = {
      "SmiteshP/nvim-navic",
      "nvim-tree/nvim-web-devicons",
    },
    config = true,
  },

  -- csv highlight
  {
    "mechatroner/rainbow_csv",
    lazy = true,
  },

  -- smooth scroll
  {
    "karb94/neoscroll.nvim",
    config = function()
      require("neoscroll").setup {}
    end,
  },

  -- add doc code
  {
    "danymat/neogen",
    config = true,
    init = function()
      vim.keymap.set(
        "n",
        "<Leader>gd",
        ':lua require("neogen").generate()<CR>',
        { silent = true, desc = "Generate Documentation" }
      )
    end,
  },

  -- install odoo snippets
  {
    "mstuttgart/vscode-odoo-snippets",
    event = "InsertEnter",
    dependencies = {
      "L3MON4D3/LuaSnip",
    },
    config = function()
      require("luasnip.loaders.from_vscode").lazy_load()
    end,
  },

  -- tmux integration
  {
    "christoomey/vim-tmux-navigator",
    lazy = false,
  },

  -- persiste sessions
  {
    'folke/persistence.nvim',
    event = 'BufReadPre',
    opts = { options = { 'buffers', 'curdir', 'tabpages', 'winsize', 'help', 'globals' } },
    -- stylua: ignore
    keys = {
      { '<leader>qs', function() require('persistence').load() end,                desc = 'Restore Session' },
      { '<leader>ql', function() require('persistence').load({ last = true }) end, desc = 'Restore Last Session' },
      { '<leader>qd', function() require('persistence').stop() end,                desc = 'Don\'t Save Current Session' },
    },
  },

}

return plugins
