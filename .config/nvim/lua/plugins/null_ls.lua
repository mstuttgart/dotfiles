-- format code
--
local plugin = {
    'jose-elias-alvarez/null-ls.nvim',
    event = { 'BufReadPre', 'BufNewFile' },
    dependencies = {
        'williamboman/mason.nvim',
        'jay-babu/mason-null-ls.nvim',
    },
    init = function()
        vim.keymap.set('n', '<leader>fm', vim.lsp.buf.format, { desc = '[F]ormat File' })
    end,
    opts = function()
        local nls = require('null-ls')
        return {
            root_dir = require('null-ls.utils').root_pattern('.null-ls-root', '.neoconf.json', 'Makefile', '.git'),
            sources = {
                nls.builtins.formatting.beautysh,
                nls.builtins.formatting.stylua,
                nls.builtins.formatting.isort,
                nls.builtins.formatting.autopep8,
                nls.builtins.formatting.xmlformat.with {
                    arg = { '--blanks', '--indent 4' },
                },
                nls.builtins.formatting.xmllint.with {
                    { '--format', '-' },
                },
                nls.builtins.formatting.yamlfmt,
                nls.builtins.formatting.prettier.with {
                    prefer_local = 'node_modules/.bin',
                },
                nls.builtins.formatting.eslint.with {
                    prefer_local = 'node_modules/.bin',
                },
                nls.builtins.diagnostics.pylint.with {
                    diagnostic_config = { underline = false, virtual_text = false, signs = true },
                    prefer_local = '.venv/bin',
                },
                nls.builtins.diagnostics.ansiblelint,
                nls.builtins.diagnostics.eslint.with {
                    prefer_local = 'node_modules/.bin',
                },
                nls.builtins.diagnostics.shellcheck,
                nls.builtins.code_actions.eslint.with {
                    prefer_local = 'node_modules/.bin',
                },
            },
        }
    end,
}

return plugin
