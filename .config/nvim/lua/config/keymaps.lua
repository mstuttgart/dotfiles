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

-- Don't copy the replaced text after pasting in visual mode
    -- https://vim.fandom.com/wiki/Replace_a_word_with_yanked_text#Alternative_mapping_for_paste
set({ 'v', 'x' }, 'p', 'p:let @+=@0<CR>:let @"=@0<CR>', { desc = "Dont copy replaced text" })

-- better indenting
set('v', '<', '<gv')
set('v', '>', '>gv')

-- lazy
set('n', '<leader>L', '<cmd>:Lazy<cr>', { desc = 'Lazy' })

-- navegate in insert <ctrl> hjkl keys
set('i', '<C-h>', '<Left>', { desc = 'Move left' })
set('i', '<C-j>', '<Down>', { desc = 'Move down' })
set('i', '<C-k>', '<Up>', { desc = 'Move up' })
set('i', '<C-l>', '<Right>', { desc = 'Move right' })

-- Diagnostic keymaps
set('n', '[d', vim.diagnostic.goto_prev, { desc = 'Go to previous diagnostic message' })
set('n', ']d', vim.diagnostic.goto_next, { desc = 'Go to next diagnostic message' })
set('n', '<leader>dm', vim.diagnostic.open_float, { desc = 'Open floating diagnostic message' })
set('n', '<leader>dl', vim.diagnostic.setloclist, { desc = 'Open diagnostics list' })

-- split editor
set('n', '<leader>wh', '<C-u>split<CR>', { desc = 'Split horizontal' })
set('n', '<leader>wv', '<C-u>vsplit<CR>', { desc = 'Split vertical' })

-- quit
set("n", "<leader>qq", "<cmd>qa<cr>", { desc = "Quit all" })
