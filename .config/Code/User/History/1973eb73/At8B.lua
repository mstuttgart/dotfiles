---@type MappingsTable
local M = {}

M.general = {
  n = {
    [";"] = { ":", "enter command mode", opts = { nowait = true } },
    ["<C-s>"] = { "<cmd> wa <CR>", "Save file" },
    ["<leader>L"] = { "<cmd>:Lazy<cr>", "Lazy" },
    ['<esc>'] = { "<cmd>noh<cr><esc>", 'Escape and clear hlsearch' },
  },
  i = {
    ["<C-s>"] = { "<cmd> wa <CR><ESC>", "Save file" },
    ['<esc>'] = { "<cmd>noh<cr><esc>", 'Escape and clear hlsearch' },
  },
  v = {
    [">"] = { ">gv", "indent" },
    ["<"] = { "<gv", "indent" },
  },
}
--
-- more keybinds!

return M
