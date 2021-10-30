" vim-plug pluggin
let g:plugged_home = '~/.config/nvim/plugged'

"------------ Plugins list ----------------

" Plugins List
call plug#begin(g:plugged_home)

  " UI related
  Plug 'scrooloose/nerdtree'
  Plug 'vim-airline/vim-airline'
  Plug 'vim-airline/vim-airline-themes'

  " Theme gruvbox
  Plug 'morhetz/gruvbox'
  Plug 'ajmwagar/vim-deus'

  " Better Visual Guide
  Plug 'Yggdroot/indentLine'

  " Syntax check and autoformat
  Plug 'w0rp/ale'

  " Syntax support and python syntax
  Plug 'sheerun/vim-polyglot'
  Plug 'davidhalter/jedi-vim'

  " Auto close chars like '(', '{', '[' and ""
  Plug 'jiangmiao/auto-pairs'

  " Comment code
  Plug 'scrooloose/nerdcommenter'

  " Snippets plugins
  Plug 'SirVer/ultisnips'

  " Markdown support
  Plug 'godlygeek/tabular'
  Plug 'plasticboy/vim-markdown'

  call plug#end()

"------------ General Settings ----------------

" Configurations Part
" UI configuration
syntax on
syntax enable

" Open new split panes to right and bottom, which feels more natural than Vim’s default
set splitbelow
set splitright

" Set encoding
set encoding=utf-8

" Load filetype-specific indent files
filetype plugin indent on

" True Color Support if it's avaiable in terminal
if has("termguicolors")
    set termguicolors
endif

" Set background
set background=dark

" Set colorscheme
colorscheme gruvbox

" Show line number
set number

" Active relative number
set relativenumber

" Not close unsaved buffers when open new file
set hidden

" Hide mode name when change mode
" Use when AirLine is be installed
set noshowmode

" Mouse copy support
set mouse=a

" Improve speed when scrooling and use macros
" Redraw only when you need
set nolazyredraw

" Turn off backup
set nobackup
set nowritebackup

" Search configuration
set ignorecase                    " ignore case when searching
set smartcase                     " turn on smartcase

" Highlight matching [{()}]
set showmatch         

" Search while characters are entered
set incsearch            

" Highlight all matches
set hlsearch           

" Turn off search highlight
nnoremap <leader><space> :nohlsearch<CR>

"------------ Ale Settings ----------------

" Ale not run in opening file
let g:ale_lint_on_enter = 0

" Ale run when save the file"
let g:ale_lint_on_text_changed = 'never'

let g:ale_echo_msg_error_str = 'E'
let g:ale_echo_msg_warning_str = 'W'
let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'

" Ale configure linters
let g:ale_linters = {
\  'python': ['flake8'],
\}

" Ale configure autoformat tools
let g:ale_fixers = {
\   '*': ['remove_trailing_lines', 'trim_whitespace'],
\   'python': ['autopep8', 'isort'],
\}

" Show error list
let g:ale_open_list = 1

"------------ IndentLine Settings ----------------

let g:indentLine_enabled = 1
let g:indentLine_concealcursor = 0
let g:indentLine_char = '┆'
let g:indentLine_faster = 1

" Indent char to different indent levels
let g:indentLine_char_list = ['|', '¦', '┆', '┊']

"------------ Syntax Highlight Settings ----------------

" Syntax highlight
" Default highlight is better than polyglot
let g:polyglot_disabled = ['python']
let python_highlight_all = 1

" jedi-vim
let g:jedi#popup_on_dot = 0
let g:jedi#show_call_signatures = "0"
let g:jedi#completions_command = "<C-Space>"

"------------ NERDTree Settings ----------------

" NERDTree and nerd_tree_tabs configuration
nnoremap <silent> <F2> :NERDTreeFind<CR>
nnoremap <silent> <F3> :NERDTreeToggle<CR>

let g:NERDTreeChDirMode=2
let g:NERDTreeIgnore=['\.rbc$', '\~$', '\.pyc$', '\.db$', '\.sqlite$', '__pycache__']
let g:NERDTreeSortOrder=['^__\.py$', '\/$', '*', '\.swp$', '\.bak$', '\~$']
let g:NERDTreeShowBookmarks=1
let g:NERDTreeMapOpenInTabSilent = '<RightMouse>'
let g:NERDTreeWinSize = 50

"------------ Airline Settings ----------------

let g:airline_theme = 'gruvbox' 
let g:airline_left_sep  = ''
let g:airline_right_sep = ''

let g:airline#extensions#virtualenv#enabled = 1
let g:airline#extensions#ale#enabled = 1
let g:airline#extensions#ale#error_symbol = 'E:'
let g:airline#extensions#ale#warning_symbol = 'W:'


"-------------- UltiSnips Setting --------------

let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-j>"
let g:UltiSnipsJumpBackwardTrigger="<c-k>"

"------------ Specifi files settings Settings ----------------

" Number of visual spaces that a pre-existing tab is equal to.
au BufRead,BufNewFile *py set tabstop=4

" spaces for indents
au BufRead,BufNewFile *.py; set shiftwidth=4
au BufRead,BufNewFile *.py; set expandtab " turn tabs in spaces
au BufRead,BufNewFile *.py; set softtabstop=4 " number of spaces in tab when editing
au BufRead,BufNewFile *.py; set autoindent
au BufRead,BufNewFile *.py; set textwidth=79
au BufRead,BufNewFile *.py; set fileformat=unix

" Specific Python commands and settings
augroup PythonCustomization

  " highlight python self, when followed by a comma, a period or a parenth
   :autocmd FileType python syn match pythonStatement "\(\W\|^\)\@<=self\([\.,)]\)\@="
  
   " Insert shortcut to insert 'ipdb' debug command
   " pip install ipdb to work
   :autocmd FileType python nnoremap ipdb o import ipdb; ipdb.set_trace() <esc>

augroup END

" spaces for indents in javascript, html and css files
au BufRead,BufNewFile *.js,*.html,*.css; set tabstop=2
au BufRead,BufNewFile *.js,*.html,*.css; set softtabstop=2
au BufRead,BufNewFile *.js,*.html,*.css; set shiftwidth=2

" markdown settings
au BufNewFile,BufRead *.md,*.markdown setlocal filetype=ghmarkdown


