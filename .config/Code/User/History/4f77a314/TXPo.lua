-- treesitter settings
-- Highlight, edit, and navigate code

local plugin = {
    'nvim-treesitter/nvim-treesitter',
    version = false, -- last release is way too old and doesn't work on Windows
    build = ":TSUpdate",
    event = { "BufReadPre", "BufNewFile" },
    cmd = {
        "TSUpdateSync",
        "TSUpdate",
        "TSInstall",
    },
    config = function()
        require('nvim-treesitter.configs').setup {
            -- Add languages to be installed here that you want installed for treesitter
            ensure_installed = {
                'bash',
                'css',
                'html',
                'javascript',
                'json',
                'lua',
                'markdown_inline',
                'markdown',
                'python',
                'query',
                'regex',
                'toml',
                'xml',
                'yaml',
            },
            -- Autoinstall languages that are not installed. Defaults to false (but you can change for yourself!)
            auto_install = true,
            highlight = { enable = true },
            indent = {
                enable = true,
                disable = { 'python' },
            },
            context_commentstring = {
                enable = false,
                enable_autocmd = false,
                config = {
                    python = '# %s',
                },
            },
        }
    end,
}

return plugin
