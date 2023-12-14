-- Configure mason to autoinstall linters and formatters
local plugins = {
  "williamboman/mason.nvim",
  dependencies = {
    "williamboman/mason-lspconfig.nvim",
    "WhoIsSethDaniel/mason-tool-installer.nvim",
  },
  config = function()
    -- onverride mason icons
    require("mason").setup {
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗",
        },
      },
    }

    -- auto install LSP
    require("mason-lspconfig").setup {
      ensure_installed = {
        "pyright",
        "html",
        "cssls",
        "lua_ls",
        "bashls",
        "ansiblels",
      },
      -- auto-install configured servers (with lspconfig)
      automatic_installation = true,
    }

    require("mason-tool-installer").setup {
      ensure_installed = {
        -- linters
        "eslint_d",
        "shellcheck",
        "pylint",

        -- formatters
        "autopep8",
        "isort",
        "prettier",
        "shfmt",
        "stylua",
        "xmlformatter",
        "yamlfmt",
      },
    }
  end,
}

return plugins
