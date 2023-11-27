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
      vim.o.background="light"
      vim.cmd.colorscheme "everforest"
    end,
  },
}

return plugins
