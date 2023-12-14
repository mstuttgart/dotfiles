-- Use Neovim as a language server to inject LSP diagnostics, code actions, and more via Lua.

local plugin = {

    "nvimtools/none-ls.nvim",
    lazy = false,
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      'nvim-lua/plenary.nvim',
    },
    init = function()
      vim.keymap.set("n", "<leader>cf", vim.lsp.buf.format, { desc = "Format File" })
    end,
    opts = function()
      local nls = require "null-ls"
      return {
        root_dir = require("null-ls.utils").root_pattern(".null-ls-root", ".neoconf.json", "Makefile", ".git"),
        sources = {
          -- formatters
            arg = { "--blanks", "--indent 4" },
            diagnostic_config = { underline = false, virtual_text = false, signs = true },
            prefer_local = ".venv/bin",
            prefer_local = "node_modules/.bin",
            prefer_local = "node_modules/.bin",
            prefer_local = "node_modules/.bin",
          -- linters
          },
          },
          },
          },
          },
          nls.builtins.code_actions.eslint.with {
          nls.builtins.diagnostics.ansiblelint,
          nls.builtins.diagnostics.eslint.with {
          nls.builtins.diagnostics.pylint.with {
          nls.builtins.diagnostics.shellcheck,
          nls.builtins.formatting.autopep8,
          nls.builtins.formatting.isort,
          nls.builtins.formatting.prettier.with {
          nls.builtins.formatting.shfmt,
          nls.builtins.formatting.stylua,
          nls.builtins.formatting.xmlformat.with {
          nls.builtins.formatting.yamlfmt,
        },
      }
    end
}

return plugin
