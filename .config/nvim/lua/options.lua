-- General Settings --

local g = vim.g
local opt = vim.opt
local cmd = vim.cmd

-- set encoding
opt.encoding = 'utf-8'
opt.fileencoding = 'utf-8'
opt.fileencodings = 'utf-8'

-- disable compatibility with vi
opt.compatible = false

-- enable mouse
opt.mouse = 'a'
opt.mousemodel = 'popup'

-- use system clipboard
opt.clipboard = 'unnamedplus'

-- expand tabs into spaces
opt.expandtab = true
opt.shiftwidth = 2
opt.softtabstop = 0
opt.tabstop = 2

-- show cursor line
opt.cursorline = true

-- indent when moving to the next line while writing code
opt.autoindent = true
opt.smartindent = true

-- enable hidden buffers
opt.hidden = true

-- enable number
opt.number = true

-- highlight matching [{()}]
opt.showmatch = true

-- open new split panes to right and bottom
opt.splitbelow = true
opt.splitright = true

-- search configuration

 -- ignore case
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true

 -- highligth search
opt.hlsearch = true

-- theme settings
opt.termguicolors = true

vim.api.nvim_command([[

" disable folding code
autocmd BufWritePost,BufEnter * set nofoldenable

]])
