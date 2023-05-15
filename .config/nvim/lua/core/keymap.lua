local set = vim.keymap.set

local ns = { silent = true, noremap = true }

-- leader/local leader
vim.g.mapleader = " "

-- save and exit easier
set('n', '<leader>w', ':update<CR>', ns)

-- show config file
set('n', '<leader>ev', ':vsplit $MYVIMRC<CR>', ns)

-- Select all
set('n', '<C-a>', 'gg<S-v>G')

-- tab navegation
set('n', '<Tab>', ':tabnext<CR>', ns)
set('n', '<S-Tab>', ':tabprevious<CR>', ns)

set('n', '<Up>', '<NOP>', ns)
set('n', '<Down>', '<NOP>', ns)
set('n', '<Left>', '<NOP>', ns)
set('n', '<Right>', '<NOP>', ns)

-- split editor
set('n', '<leader>h', '<C-u>split<CR>', ns)
set('n', '<leader>v', '<C-u>vsplit<CR>', ns)

set('n',  '<leader>tg', ':SymbolsOutline<CR>', ns)
