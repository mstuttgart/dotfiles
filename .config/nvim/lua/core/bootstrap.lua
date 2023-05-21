-- Install lazy.nvim automatically

local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        'git',
        'clone',
        '--filter=blob:none',
        'https://github.com/folke/lazy.nvim.git',
        '--branch=stable', -- latest stable release
        lazypath,
    })
end

vim.opt.rtp:prepend(lazypath)

local opts = {
    ui = {
        custom_keys = { false },
    },
    install = {
        colorscheme = { 'everforest' },
        -- install missing plugins on startup. This doesn't increase startup time.
        missing = true,
    },
    performance = {
        rtp = {
            disabled_plugins = {
                'gzip',
                'netrwPlugin',
                'tarPlugin',
                'tohtml',
                'tutor',
                'zipPlugin',
                'rplugin',
                'editorconfig',
                'matchparen',
                'matchit',
            },
        },
    },
    checker = {
        enabled = true,
    },
}

-- Load the plugins and options
require('lazy').setup('plugins', opts)
