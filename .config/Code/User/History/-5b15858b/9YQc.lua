-- configure nulll-ls to formatters and linters

local null_ls = require "null-ls"

local formatting = null_ls.builtins.formatting
local lint = null_ls.builtins.diagnostics

local sources = {
    -- formatters
    formatting.shfmt,
    formatting.stylua,
    formatting.isort,
    formatting.autopep8,
    formatting.xmlformat.with {
        arg = { "--blanks", "--indent 4" },
    },
    formatting.yamlfmt,
    formatting.prettier.with {
        prefer_local = "node_modules/.bin",
    },

    -- linters
    nls.builtins.diagnostics.pylint.with {
        diagnostic_config = { underline = false, virtual_text = false, signs = true },
        prefer_local = ".venv/bin",
    },
    nls.builtins.diagnostics.ansiblelint,
    nls.builtins.diagnostics.eslint.with {
        prefer_local = "node_modules/.bin",
    },
    nls.builtins.diagnostics.shellcheck,
    nls.builtins.code_actions.eslint.with {
        prefer_local = "node_modules/.bin",
    },
}

null_ls.setup {
    debug = true,
    sources = sources,
}
