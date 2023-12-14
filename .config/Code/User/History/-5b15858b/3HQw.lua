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
    lint.pylint.with {
        diagnostic_config = { underline = false, virtual_text = false, signs = true },
        prefer_local = ".venv/bin",
    },
    lint.ansiblelint,
    lint.eslint.with {
        prefer_local = "node_modules/.bin",
    },
    lint.shellcheck,
}

null_ls.setup {
    debug = true,
    sources = sources,
}
