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
-- require('everforest').load()

-- vim.cmd[[hi NeoTreeNormal guibg=NONE ctermbg=NONE]]
-- vim.cmd[[hi NeoTreeEndOfBuffer guibg=NONE ctermbg=NONE]]

vim.api.nvim_command([[

" html
" for html files, 2 spaces
autocmd Filetype html,css setlocal ts=2 sw=2 expandtab

" yaml
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab

" .conf
autocmd FileType *.conf setl ft=conf

augroup vimrc-javascript
  autocmd!
  autocmd FileType javascript setl tabstop=4|setl shiftwidth=4|setl expandtab softtabstop=4
augroup END

" python
" vim-python
augroup vimrc-python
  autocmd!
  autocmd FileType python setlocal expandtab shiftwidth=4 tabstop=8 colorcolumn=79
      \ formatoptions+=croq softtabstop=4
      \ cinwords=if,elif,else,for,while,try,except,finally,def,class,with
augroup END

]])
