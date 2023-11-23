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
    priority = 1000,
    config = function()
      vim.cmd [[colorscheme catppuccin]]
    end,
  },
  {
    "maxmx03/solarized.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      require("solarized").setup {
        transparent = false, -- enable transparent background
        styles = {
          comments = { italic = true, bold = false },
          functions = { italic = true },
          variables = { italic = false },
        },
      }
      vim.o.background = "light" -- or 'light'

      vim.cmd.colorscheme "solarized"
    end,
  },
  {
    "sainnhe/everforest",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.g.everforest_background = "hard"

    --   -- For better performance
    --   -- vim.g.everforest_better_performance = 1
    --   vim.cmd [[colorscheme everforest]]
    -- end,
  },
}

return plugins
