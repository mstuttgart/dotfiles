-- local autocmd = vim.api.nvim_create_autocmd

-- Auto resize panes when resizing nvim window
-- autocmd("VimResized", {
--   pattern = "*",
--   command = "tabdo wincmd =",
-- })
--
 local opt = vim.opt

-- opt.cursorline = true -- Enable highlighting of the current line
-- opt.expandtab = true -- Use spaces instead of tabstop
-- opt.list = true -- Show some invisible characters (tabs...
-- opt.mouse = 'a' -- Enable mouse mode


-- local opt = vim.opt

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
