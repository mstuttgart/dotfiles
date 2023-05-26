-- general keybinds

local set = vim.keymap.set

-- Remap for dealing with word wrap
set('n', 'k', "v:count == 0 ? 'gk' : 'k'", { expr = true, silent = true })
set('n', 'j', "v:count == 0 ? 'gj' : 'j'", { expr = true, silent = true })

-- split editor
-- set('n', '<leader>h', '<C-u>split<CR>', { desc = 'Split horizontal' })
-- set('n', '<leader>v', '<C-u>vsplit<CR>', { desc = 'Split vertical' })

-- taken from lazyVim
--
-- Clear search with <esc>
set({ 'i', 'n' }, '<esc>', '<cmd>noh<cr><esc>', { desc = 'Escape and clear hlsearch' })

-- Clear search, diff update and redraw
-- taken from runtime/lua/_editor.lua
set(
    'n',
    '<leader>ur',
    '<Cmd>nohlsearch<Bar>diffupdate<Bar>normal! <C-L><CR>',
    { desc = 'Redraw / clear hlsearch / diff update' }
)

-- save file
set({ 'i', 'v', 'n', 's' }, '<C-s>', '<cmd>wa<cr><esc>', { desc = 'Save file' })

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

set('n', '<leader>bl', '<cmd>:bnext<cr>', { desc = 'Move to next buffer' })
set('n', '<leader>bh', '<cmd>:bprevious<cr>', { desc = 'Move to previuos' })
set('n', '<leader>bq', '<cmd>:bp <BAR> bd #<cr>', { desc = 'Close current buffer' })
set('n', '<leader>bL', '<cmd>:ls<cr>', { desc = 'List open buffers' })

-- search word under cursos
set({ 'n', 'x' }, 'gw', '*N', { desc = 'Search word under cursor' })

-- better indenting
set('v', '<', '<gv')
set('v', '>', '>gv')

-- lazy
set('n', '<leader>L', '<cmd>:Lazy<cr>', { desc = 'Lazy' })

-- Diagnostic keymaps
set('n', '[d', vim.diagnostic.goto_prev, { desc = 'Go to previous diagnostic message' })
set('n', ']d', vim.diagnostic.goto_next, { desc = 'Go to next diagnostic message' })
set('n', '<leader>e', vim.diagnostic.open_float, { desc = 'Open floating diagnostic message' })
set('n', '<leader>q', vim.diagnostic.setloclist, { desc = 'Open diagnostics list' })

-- tabs
set('n', '<leader><tab>l', '<cmd>tablast<cr>', { desc = 'Last Tab' })
set('n', '<leader><tab>f', '<cmd>tabfirst<cr>', { desc = 'First Tab' })
set('n', '<leader><tab><tab>', '<cmd>tabnew<cr>', { desc = 'New Tab' })
set('n', '<leader><tab>]', '<cmd>tabnext<cr>', { desc = 'Next Tab' })
set('n', '<leader><tab>d', '<cmd>tabclose<cr>', { desc = 'Close Tab' })
set('n', '<leader><tab>[', '<cmd>tabprevious<cr>', { desc = 'Previous Tab' })
