-- general keybinds

local opts = { noremap = true, silent = true }

local term_opts = { silent = true }

-- Shorten function name
local set = vim.keymap.set

--Remap space as leader key
vim.g.mapleader = " "
vim.g.maplocalleader = " "


-- taken from lazyVim

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