local plugin = {
  "nvim-pack/nvim-spectre",
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  event = "VeryLazy",
  keys = {
    { "<leader>cs", '<cmd>lua require("spectre").toggle()<CR>', desc = "Toggle Spectre" },
  },
  config = function()
    require("spectre").setup()
  end,
}

return plugin
