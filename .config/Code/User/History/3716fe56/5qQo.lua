-- general plugins
local plugins = {

  -- csv highlight
  {
    "mechatroner/rainbow_csv",
    event = "VeryLazy",
  },

  -- word highlight
  {
    "echasnovski/mini.cursorword",
    event = "VeryLazy",
    version = "*",
    config = function()
      require("mini.cursorword").setup()
    end,
  },

  -- comment
  {
    "echasnovski/mini.comment",
    version = "*",
    event = "VeryLazy",
    opts = {},
    config = function()
      require("mini.comment").setup {
        options = {
          -- Whether to ignore blank lines
          ignore_blank_line = true,
        },
      }
    end,
  },

  -- surround
  {
    "kylechui/nvim-surround",
    version = "*",
    event = "VeryLazy",
    dependencies = {
      'nvim-treesitter/nvim-treesitter',
      "nvim-treesitter/nvim-treesitter-textobjects",
    },
    config = function()
      require("nvim-surround").setup()
    end,
  },

  -- better scape shortcuts
  {
    "max397574/better-escape.nvim",
    event = "InsertEnter",
    config = function()
      require("better_escape").setup()
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

  -- Seamless navigation between tmux panes and vim splits
  {
    "christoomey/vim-tmux-navigator",
  },

  -- fuzzy finder
  {
    "junegunn/fzf.vim",
    "junegunn/fzf",
    },
  
    -- smooth scroll
    {
      "karb94/neoscroll.nvim",
      config = function()
        require("neoscroll").setup {}
      end,
    },

}

return plugins
