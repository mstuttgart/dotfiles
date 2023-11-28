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

  -- surround
  {
    "kylechui/nvim-surround",
    version = "*",
    event = "VeryLazy",
    dependencies = {
      "nvim-treesitter/nvim-treesitter",
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
  -- {
  --   "christoomey/vim-tmux-navigator",
  -- },
  -- {
  --   "mrjones2014/smart-splits.nvim",
  -- },
  --
  -- {
  --   "Lilja/zellij.nvim",
  --   keys = {
  --     { "<alt>j", "<Cmd>ZellijNavigate Up<CR>",   desc = "Move Zellij Up Panel" },
  --     { "<alt>k", "<Cmd>ZellijNavigate Down<CR>", desc = "Move Zellij Down Panel" },
  --   },
  --   config = function()
  --     require("zellij").setup {
  --       -- vimTmuxNavigatorKeybinds = true, -- Will set keybinds like <C-h> to left
  --     }
  --   end,
  -- },

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

  -- navic complement to breadcumbs
  {
    "utilyre/barbecue.nvim",
    version = "*",
    dependencies = {
      "SmiteshP/nvim-navic",
      "nvim-tree/nvim-web-devicons",
    },
    config = true,
  },

  -- Non-intrusive notification system for neovim
  {
    "vigoux/notifier.nvim",
    config = function()
      require("notifier").setup()
    end,
  },
}

return plugins

