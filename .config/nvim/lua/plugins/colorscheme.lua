-- colorschemes

local plugins = {
  {
    "Shatur/neovim-ayu",
    lazy = true,
  },
  {
    "catppuccin/nvim",
    name = "catppuccin",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd [[colorscheme catppuccin]]
    -- end,
  },

  {
    "Mofiqul/dracula.nvim",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd [[colorscheme dracula]]
    -- end,
  },
  {
    "folke/tokyonight.nvim",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd [[colorscheme tokyonight]]
    -- end,
  },
  {
    "navarasu/onedark.nvim",
    lazy = true,
  },
  {
    "sainnhe/everforest",
    priority = 1000,
    config = function()
      -- vim.g.everforest_background = "medium"

      -- For better performance
      -- vim.g.everforest_better_performance = 1
      vim.cmd [[colorscheme everforest]]
    end,
  },
}

return plugins
