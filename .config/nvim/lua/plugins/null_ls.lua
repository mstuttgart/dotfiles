-- format code
--
local plugin = {
    'jose-elias-alvarez/null-ls.nvim',
    event = { 'BufReadPre', 'BufNewFile' },
    dependencies = { 'mason.nvim' },
    opts = function()
        local nls = require('null-ls')
        return {
            root_dir = require('null-ls.utils').root_pattern('.null-ls-root', '.neoconf.json', 'Makefile', '.git'),
            sources = {
                nls.builtins.formatting.fish_indent,
                nls.builtins.formatting.stylua,
                nls.builtins.formatting.shfmt,
                nls.builtins.formatting.isort,
                nls.builtins.formatting.autopep8,
                nls.builtins.formatting.xmlformat,
                nls.builtins.formatting.yamlfmt,
                nls.builtins.formatting.prettier.with {
                    prefer_local = 'node_modules/.bin',
                },
                nls.builtins.formatting.eslint.with {
                    prefer_local = 'node_modules/.bin',
                },
                nls.builtins.diagnostics.pylint.with {
                    prefer_local = '.venv/bin',
                },
                nls.builtins.diagnostics.fish,
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
