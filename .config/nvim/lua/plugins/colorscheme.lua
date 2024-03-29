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
      -- vim.o.background = "light"
      vim.cmd.colorscheme "everforest"
    end,
  },
  {
    "sainnhe/gruvbox-material",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.g.gruvbox_material_background = "hard"
    --   vim.cmd.colorscheme "gruvbox-material"
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
  {
    "Shatur/neovim-ayu",
    lazy = true,
    -- priority = 1000,
    -- config = function()
    --   vim.cmd.colorscheme "ayu"
    -- end,
  },
}

return plugins
