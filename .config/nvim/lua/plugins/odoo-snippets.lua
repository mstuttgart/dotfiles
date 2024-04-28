local plugin = {
  "mstuttgart/vscode-odoo-snippets",
  event = "InsertEnter",
  dependencies = {
    "L3MON4D3/LuaSnip",
  },
  config = function()
    require("luasnip.loaders.from_vscode").lazy_load()
  end,
}

return plugin
