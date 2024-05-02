-- cursorword
local plugin = {
  "echasnovski/mini.cursorword",
  event = "VeryLazy",
  version = "*",
  config = function()
    require("mini.cursorword").setup()
  end,
}

return plugin
