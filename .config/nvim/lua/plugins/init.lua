-- general plugins
local plugins = {

  -- lua functions that many plugins use
  {
    "nvim-lua/plenary.nvim",
  },

  -- better scape shortcuts
  {
    "max397574/better-escape.nvim",
    event = "InsertEnter",
    config = function()
      require("better_escape").setup()
    end,
  },

  -- A fancy, configurable, notification manager for NeoVim
  {
    "rcarriga/nvim-notify",
    event = "VeryLazy",
  },

  -- Neovim plugin to improve the default vim.ui interfaces
  {
    "stevearc/dressing.nvim",
    event = "VeryLazy",
  },

  -- smooth scroll
  {
    "karb94/neoscroll.nvim",
    config = function()
      require("neoscroll").setup {}
    end,
  },

  --   -- helping you establish good command workflow and quit bad habit
  --   {
  --     "m4xshen/hardtime.nvim",
  --     dependencies = { "MunifTanjim/nui.nvim", "nvim-lua/plenary.nvim" },
  --     opts = {},
  --     config = function()
  --       require("hardtime").setup {}
  --     end,
  --   },
}

return plugins
