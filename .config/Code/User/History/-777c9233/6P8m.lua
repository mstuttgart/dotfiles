-- general keybinds

local opts = { noremap = true, silent = true }

local term_opts = { silent = true }

-- Shorten function name
local keymap = vim.api.nvim_set_keymap

--Remap space as leader key
keymap("", "<Space>", "<Nop>", opts)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Modes
--  normal_mode = "n",
--  insert_mode = "i",
--  visual_mode = "v",
--  visual_block_mode = "x",
--  term_mode = "t",
--  command_mode = "c",

-- Better window navigation
keymap("n", "<C-h>", "<C-w>h", opts) -- left window
keymap("n", "<C-k>", "<C-w>k", opts) -- up window
keymap("n", "<C-j>", "<C-w>j", opts) -- down window
keymap("n", "<C-l>", "<C-w>l", opts) -- right window

-- Resize with arrows when using multiple windows
keymap("n", "<C-Up>", ":resize -2<CR>", opts)
keymap("n", "<c-down>", ":resize +2<cr>", opts)
keymap("n", "<c-right>", ":vertical resize -2<cr>", opts)
keymap("n", "<c-left>", ":vertical resize +2<cr>", opts)

-- navigate buffers
keymap("n", "<tab>", ":bnext<cr>", opts) -- Next Tab 
keymap("n", "<s-tab>", ":bprevious<cr>", opts) -- Previous tab
keymap("n", "<leader>h", ":nohlsearch<cr>", opts) -- No highlight search

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
