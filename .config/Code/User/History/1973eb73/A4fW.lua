---@type MappingsTable
local M = {}

M.general = {
  n = {
    [";"] = { ":", "enter command mode", opts = { nowait = true } },
    ["<C-s>"] = { "<cmd> wa <CR>", "Save file" },
        ["<leader>L"] = { "<cmd>:Lazy<cr>", "Lazy" },
    ['<esc>'] = {}
  },
  i = {
    ["<C-s>"] = { "<cmd> wa <CR><ESC>", "Save file" },
  },
  v = {
    [">"] = { ">gv", "indent" },
  },
}
-- 
-- more keybinds!

return M
