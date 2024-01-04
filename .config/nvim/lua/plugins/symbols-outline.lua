local plugin = {
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
}

return plugin
