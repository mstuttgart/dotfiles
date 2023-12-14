vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {

  

  -- Find the enemy and replace them with dark power.
  -- {
  --   "nvim-pack/nvim-spectre",
  --   build = false,
  --   cmd = "Spectre",
  --   opts = { open_cmd = "noswapfile vnew" },
  --       -- stylua: ignore
  --       keys = {
  --           { "<leader>sr", function() require("spectre").open() end, desc = "Replace in files (Spectre)" },
  --       },
  -- },

  



  -- see code tags
  {
    "simrat39/symbols-outline.nvim",
    cmd = "SymbolsOutline",
    keys = {
      { "<leader>ct", "<cmd>SymbolsOutline<cr>", desc = "Code Tags (Symbols Outline)" },
    },
    config = function()
      require("symbols-outline").setup {
        vim.api.nvim_create_autocmd("BufEnter", {
          pattern = "*",
          command = "hi SymbolsOutlineConnector gui=none guifg=vim.g.foreground",
        }),
      }
    end,
  },


}

return plugins
