-- Configure mason to autoinstall linters and formatters
local plugins = {
  "williamboman/mason.nvim",
  cmd = { "Mason", "MasonInstall", "MasonInstallAll", "MasonUpdate" },
  dependencies = {
    "williamboman/mason-lspconfig.nvim",
    "WhoIsSethDaniel/mason-tool-installer.nvim",
  },
  opts = {
    PATH = "skip",
    ui = {
      icons = {
        package_installed = "✓",
        package_pending = "➜",
        package_uninstalled = "✗",
      },
    },
    --   -- auto-install configured servers (with lspconfig)
      -- automatic_installation = true,
  },
  config = function(_, opts)
    -- setup mason settings
    require("mason").setup(opts)

    local ensure_installed = {
      -- lsp
      "ansible-language-server",
      "bash-language-server",
      "css-lsp",
      "html-lsp",
      "lua-language-server",
      "pyright",
      "typescript-language-server",
      -- linters
      -- "eslint_d",
      -- "pylint",
      -- "shellcheck",
      -- -- formatters
      -- "autopep8",
      -- "isort",
      -- "prettier",
      -- "shfmt",
      -- "stylua",
      -- "xmlformatter",
      -- "yamlfmt",
    }

    auto install LSP
    require("mason-lspconfig").setup {
      ensure_installed = {
        "ansiblels",
        "bashls",
        "cssls",
        "html",
        "lua_ls",
        "pyright",
        "tsserver"
      },
      -- auto-install configured servers (with lspconfig)
      automatic_installation = true,
    }

    require("mason-tool-installer").setup {
      ensure_installed = {
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
        "xmlformatter",
        "yamlfmt",
      },
    }

    -- custom nvchad cmd to install all mason binaries listed
    -- https://github.com/NvChad/NvChad
    vim.api.nvim_create_user_command("MasonInstallAll", function()
      vim.cmd("MasonInstall " .. table.concat(ensure_installed, " "))
    end, {})

    vim.g.mason_binaries_list = ensure_installed
  end,
}

return plugins
