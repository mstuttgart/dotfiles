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
        transparent_background_level = 1,
      }
      vim.cmd.colorscheme "everforest"
    end,
  },
  {
    "sainnhe/gruvbox-material",
    lazy=true,
    -- priority = 1000,
    -- config = function()
    --   vim.g.gruvbox_material_background = "hard"
    --   vim.cmd.colorscheme "gruvbox-material"
    -- end,
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
}

return plugins
