-- snippet plugin
local plugin = {
  "L3MON4D3/LuaSnip",
  dependencies = {
    "rafamadriz/friendly-snippets",
    "mstuttgart/vscode-odoo-snippets",
  },
  opts = {
    history = true,
    updateevents = "TextChanged,TextChangedI",
  },
  keys = function()
    return {}
  end,
  config = function()
    require("luasnip.loaders.from_vscode").lazy_load()
  end,
}

return plugin
