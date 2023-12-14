local null_ls = require "null-ls"

local b = null_ls.builtins

local sources = {

  -- webdev stuff
  b.formatting.deno_fmt, -- choosed deno for ts/js files cuz its very fast!

  -- Lua
  b.formatting.stylua,
  b.formatting.shfmt,
  b.formatting.isort,
  b.formatting.autopep8,
  b.formatting.xmllint.with {
    args = {'--format', '-'},
  },
  b.formatting.yamlfmt,
  b.formatting.prettier.with {
      prefer_local = 'node_modules/.bin',
      filetypes = { "html", "markdown", "css" }
  },
  b.formatting.eslint.with {
      prefer_local = 'node_modules/.bin',
  },
  b.diagnostics.pylint.with {
      diagnostic_config = { underline = false, virtual_text = false, signs = true },
      prefer_local = '.venv/bin',
  }

}

null_ls.setup {
  debug = true,
  sources = sources,
}

