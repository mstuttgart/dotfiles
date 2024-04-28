-- Use Neovim as a language server to inject LSP diagnostics, code actions, and more via Lua.

local plugin = {
  "nvimtools/none-ls.nvim",
  lazy = false,
  event = { "BufReadPre", "BufNewFile" },
  dependencies = {
    "nvim-lua/plenary.nvim",
    "WhoIsSethDaniel/mason-tool-installer.nvim",
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
        nls.builtins.formatting.shfmt,
        nls.builtins.formatting.stylua,
        nls.builtins.formatting.isort,
        nls.builtins.formatting.black,
        nls.builtins.formatting.xmlformat,
        nls.builtins.formatting.yamlfmt,
        nls.builtins.formatting.prettier.with {
          prefer_local = "node_modules/.bin",
        },

        -- linters
        nls.builtins.diagnostics.pylint.with {
          diagnostic_config = { underline = false, virtual_text = false, signs = true },
          prefer_local = ".venv/bin",
        },
        nls.builtins.diagnostics.ansiblelint,
        -- nls.builtins.diagnostics.eslint.with {
        --   prefer_local = "node_modules/.bin",
        -- },
        nls.builtins.diagnostics.shellcheck,
        -- nls.builtins.code_actions.eslint.with {
        --   prefer_local = "node_modules/.bin",
        -- },
      },
    }
  end,
}

return plugin
