local set = vim.keymap.set

local ns = { silent = true, noremap = true }

-- remap ESCAPE key
set('i', '<C-Space>', '<esc>')

-- leader/local leader
vim.g.mapleader = " "

-- save and exit easier
set('i', '<C-s>', '<esc>:wa<CR>', ns)
set('n', '<C-s>', ':wa<CR>', ns)
-- set('i', '<C-q>', '<esc>:wqa!<CR>', ns)
-- set('n', '<C-q>', ':wqa!<CR>', ns)

-- save and exit easier
-- set('i', '<leader>w', '<esc>:wa<CR>', ns) (cau lag)
-- st('n', '<leader>w', ':wa<CR>', ns)
-- set('i', '<leader>q', '<esc>:wqa!<CR>', ns)
-- set('n', '<leader>q', ':wqa!<CR>', ns)

-- show config file
set('n', '<leader>ev', ':vsplit $MYVIMRC<CR>', ns)

-- tab navegation
set('n', '<Tab>', ':tabnext<CR>', ns)
set('n', '<S-Tab>', ':tabprevious<CR>', ns)
set('n', '<C-q>', ':tabclose', ns)

set('n', '<Up>', '<NOP>', ns)
set('n', '<Down>', '<NOP>', ns)
set('n', '<Left>', '<NOP>', ns)
set('n', '<Right>', '<NOP>', ns)

-- navigate buffers and repos
set('n', '<leader>ff', '<cmd>Telescope find_files<CR>', ns)
set('n', '<leader>fg', '<cmd>Telescope live_grep<CR>', ns)

-- split editor
set('n', '<leader>h', '<C-u>split<CR>', ns)
set('n', '<leader>v', '<C-u>vsplit<CR>', ns)

-- nvim-tree
set('n', '<Leader>ee', ':NvimTreeToggle<CR>', ns)
set('n', '<Leader>ef', ':NvimTreeFindFile<CR>', ns)

-- show tags
set('n',  '<leader>tg', ':TagbarToggle<CR>', ns)

-- inserted annotation
set('n', '<Leader>nn', ':lua require("neogen").generate()<CR>', ns)
