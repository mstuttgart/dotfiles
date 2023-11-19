-- general keybinds

-- Shorten function name
local set = vim.keymap.set

--Remap space as leader key
vim.g.mapleader = " "
vim.g.maplocalleader = " "

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

-- Resize window using <ctrl> arrow keys
set('n', '<C-Up>', '<cmd>resize +2<cr>', { desc = 'Increase window height' })
set('n', '<C-Down>', '<cmd>resize -2<cr>', { desc = 'Decrease window height' })
set('n', '<C-Left>', '<cmd>vertical resize -2<cr>', { desc = 'Decrease window width' })
set('n', '<C-Right>', '<cmd>vertical resize +2<cr>', { desc = 'Increase window width' })

-- Move to window using the <ctrl> hjkl keys
set('n', '<C-h>', '<C-w>h', { desc = 'Go to left window' })
set('n', '<C-j>', '<C-w>j', { desc = 'Go to lower window' })
set('n', '<C-k>', '<C-w>k', { desc = 'Go to upper window' })
set('n', '<C-l>', '<C-w>l', { desc = 'Go to right window' })

-- set('n', '<leader>bl', '<cmd>:bnext<cr>', { desc = 'Move to next buffer' })
-- set('n', '<leader>bh', '<cmd>:bprevious<cr>', { desc = 'Move to previuos' })
-- set('n', '<leader>bq', '<cmd>:bp <BAR> bd #<cr>', { desc = 'Close current buffer' })
-- set('n', '<leader>bL', '<cmd>:ls<cr>', { desc = 'List open buffers' })

-- Diagnostic keymaps
-- set('n', '[d', vim.diagnostic.goto_prev, { desc = 'Go to previous diagnostic message' })
-- set('n', ']d', vim.diagnostic.goto_next, { desc = 'Go to next diagnostic message' })
-- set('n', '<leader>dm', vim.diagnostic.open_float, { desc = 'Open floating diagnostic message' })
-- set('n', '<leader>dl', vim.diagnostic.setloclist, { desc = 'Open diagnostics list' })

-- split editor
set('n', '<leader>wh', '<C-u>split<CR>', { desc = 'Split horizontal' })
set('n', '<leader>wv', '<C-u>vsplit<CR>', { desc = 'Split vertical' })

-- set({ 'i', 'v', 'n' }, '<leader>fm', function()
--     vim.lsp.buf.format { async = true }
-- end, { desc = 'LSP formatting' })