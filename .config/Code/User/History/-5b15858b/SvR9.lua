-- configure nulll-ls to formatters and linters

local null_ls = require "null-ls"

local formatting = null_ls.builtins.formatting
local lint = null_ls.builtins.diagnostics

local sources = {
    -- formatters
    formatting.autopep8,
    formatting.isort,
    formatting.prettier.with {
        prefer_local = "node_modules/.bin",
    },
    formatting.shfmt,
    formatting.stylua,
    formatting.xmlformat.with {
        arg = { "--blanks", "--indent 4" },
    },
    formatting.yamlfmt,

    -- linters
    lint.ansiblelint,
    lint.eslint.with {
        prefer_local = "node_modules/.bin",
    },
    lint.pylint.with {
        diagnostic_config = { underline = false, virtual_text = false, signs = true },
        prefer_local = ".venv/bin",
    },
    lint.shellcheck,
}

null_ls.setup {
    debug = true,
    sources = sources,
}
