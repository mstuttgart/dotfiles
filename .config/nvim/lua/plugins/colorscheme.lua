-- colorschemes

local plugins = {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd.colorscheme "catppuccin"
    -- end,
  },
  {
    "neanias/everforest-nvim",
    -- lazy = true,
    priority = 1000,
    config = function()
      require("everforest").setup {
        italics = true,
      }
      vim.o.background = "light"
      vim.cmd.colorscheme "everforest"
    end,
  },
  {
    "maxmx03/solarized.nvim",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.o.background = "dark" -- or 'light'
    --   vim.cmd.colorscheme "solarized"
    -- end,
  },
  {
    "shaunsingh/nord.nvim",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd.colorscheme "nord"
    -- end,
  },
}

return plugins
