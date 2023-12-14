-- general keybinds

local set = vim.keymap.set

-- Clear search with <esc>
set({ 'i', 'n' }, '<esc>', '<cmd>noh<cr><esc>', { desc = 'Escape and clear hlsearch' })

-- save file
set({ 'i', 'v', 'n', 's' }, '<C-s>', '<cmd>wa<cr><esc>', { desc = 'Save file' })

-- search word under cursos
set({ 'n', 'x' }, 'gw', '*N', { desc = 'Search word under cursor' })

-- better indenting
set('v', '<', '<gv')
set('v', '>', '>gv')

-- lazy
set('n', '<leader>L', '<cmd>:Lazy<cr>', { desc = 'Lazy' })

-- map("n", "<C-s>", "<cmd> w <CR>")
-- map("i", "jk", "<ESC>")
-- map("n", "<C-c>", "<cmd> %y+ <CR>") -- copy whole filecontent

-- -- nvimtree
-- map("n", "<C-n>", "<cmd> NvimTreeToggle <CR>")
-- map("n", "<C-h>", "<cmd> NvimTreeFocus <CR>")

-- -- telescope
-- map("n", "<leader>ff", "<cmd> Telescope find_files <CR>")
-- map("n", "<leader>fo", "<cmd> Telescope oldfiles <CR>")
-- map("n", "<leader>fw", "<cmd> Telescope live_grep <CR>")
-- map("n", "<leader>gt", "<cmd> Telescope git_status <CR>")

-- -- bufferline, cycle buffers
-- map("n", "<Tab>", "<cmd> BufferLineCycleNext <CR>")
-- map("n", "<S-Tab>", "<cmd> BufferLineCyclePrev <CR>")
-- map("n", "<C-q>", "<cmd> bd <CR>")

-- -- comment.nvim
-- map("n", "<leader>/", function()
--   require("Comment.api").toggle.linewise.current()
-- end)

-- map("v", "<leader>/", "<ESC><cmd>lua require('Comment.api').toggle.linewise(vim.fn.visualmode())<CR>")

-- -- format
-- map("n", "<leader>fm", function()
--   require("conform").format()
-- end)
