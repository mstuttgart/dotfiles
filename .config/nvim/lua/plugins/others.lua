-- general plugins
local plugins = {

  -- csv highlight
  -- {
  --   "mechatroner/rainbow_csv",
  --   event = "VeryLazy",
  -- },

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

  -- fuzzy finder
  -- {
  --   "junegunn/fzf.vim",
  --   "junegunn/fzf",
  -- },

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
  -- {
  --   "vigoux/notifier.nvim",
  --   config = function()
  --     require("notifier").setup()
  --   end,
  -- },
  --
  {
    "NvChad/nvterm",
    config = function()
      require("nvterm").setup()

      local terminal = require "nvterm.terminal"

      -- local ft_cmds = {
      --   python = "python3 " .. vim.fn.expand('%'),
      --   ...
      --   <your commands here>
      -- }
      local toggle_modes = { "n", "t" }
      local mappings = {
        -- {
        --   "n",
        --   "<C-l>",
        --   function()
        --     terminal.send(ft_cmds[vim.bo.filetype])
        --   end,
        -- },
        {
          toggle_modes,
          "<A-h>",
          function()
            terminal.toggle "horizontal"
          end,
        },
        -- {
        --   toggle_modes,
        --   "<A-v>",
        --   function()
        --     terminal.toggle "vertical"
        --   end,
        -- },
        {
          toggle_modes,
          "<A-f>",
          function()
            terminal.toggle "float"
          end,
        },
      }
      local opts = { noremap = true, silent = true }
      for _, mapping in ipairs(mappings) do
        vim.keymap.set(mapping[1], mapping[2], mapping[3], opts)
      end
    end,
  },
}

return plugins
