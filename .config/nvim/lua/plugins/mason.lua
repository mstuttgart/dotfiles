-- Configure mason to autoinstall linters and formatters
local plugins = {
  "WhoIsSethDaniel/mason-tool-installer.nvim",
  dependencies = {
    "williamboman/mason.nvim",
  },
  config = function()
    -- setup mason settings
    require("mason").setup {
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗",
        },
      },
    }

    require("mason-tool-installer").setup {
      ensure_installed = {
        -- lsp
        "ansible-language-server",
        "bash-language-server",
        "css-lsp",
        "html-lsp",
        "lua-language-server",
        "pyright",
        "typescript-language-server",

        -- linters
        "eslint_d",
        "pylint",
        "shellcheck",

        -- formatters
        "autopep8",
        "isort",
        "prettier",
        "shfmt",
        "stylua",
        "yamlfmt",
      },

      -- auto-install configured servers (with lspconfig)
      automatic_installation = true,
    }
  end,
}

return plugins
