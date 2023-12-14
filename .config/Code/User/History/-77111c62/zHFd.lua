-- configure autocommands
local autocmd = vim.api.nvim_create_autocmd
local function augroup(name)
    return vim.api.nvim_create_augroup('lazyvim_' .. name, { clear = true })
end

-- Auto resize panes when resizing nvim window
autocmd("VimResized", {
    pattern = "*",
    command = "tabdo wincmd =",
})

-- Highlight on yank
autocmd('TextYankPost', {
    group = augroup('highlight_yank'),
    callback = function()
        vim.highlight.on_yank()
    end,
})

-- Auto create dir when saving a file, in case some intermediate directory does not exist
autocmd({ 'BufWritePre' }, {
    group = augroup('auto_create_dir'),
    callback = function(event)
        if event.match:match('^%w%w+://') then
            return
        end
        local file = vim.loop.fs_realpath(event.match) or event.match
        vim.fn.mkdir(vim.fn.fnamemodify(file, ':p:h'), 'p')
    end,
})

-- configure options
local opt = vim.opt

-- Enable auto write
opt.autowrite = true

-- Sync with system clipboard
opt.clipboard = 'unnamedplus'
opt.completeopt = 'menu,menuone,noselect'

-- Confirm to save changes before exiting modified buffer
opt.confirm = true

-- Enable highlighting of the current line
opt.cursorline = true

-- Use spaces instead of tabs
opt.expandtab = true

-- preview incremental substitute
opt.inccommand = 'nosplit'

-- Show some invisible characters (tabs... etc)
opt.list = true

-- Enable mouse mode
opt.mouse = 'a'

-- Print line number
opt.number = true

-- Relative line numbers
opt.relativenumber = false

-- Dont show mode since we have a statusline
opt.showmode = false

-- Always show the signcolumn, otherwise it would shift the text each time
opt.signcolumn = 'yes'

-- Don't ignore case with capitals
opt.smartcase = true

-- Insert indents automatically
opt.smartindent = true

-- Put new windows below current
opt.splitbelow = true

-- Put new windows right of current
opt.splitright = true

-- Number of spaces tabs count for
opt.tabstop = 2

-- True color support
opt.termguicolors = true

-- set undo files possible
opt.undofile = true
opt.undolevels = 10000

-- Save swap file and trigger CursorHold
opt.updatetime = 200

-- Command-line completion mode
opt.wildmode = 'longest:full,full'

-- Disable line wrap
opt.wrap = false