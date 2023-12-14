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
