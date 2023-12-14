-- Configure mason to autoinstall linters and formatters
local plugins = {
  "WhoIsSethDaniel/mason-tool-installer.nvim",
  dependencies = {
    -- "williamboman/mason-lspconfig.nvim",
    "williamboman/mason.nvim",
  },
  config = function()
    -- setup mason settings
    require("mason").setup({
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗"
        }
      }
    })

    -- auto install LSP
    -- require("mason-lspconfig").setup {
    --   ensure_installed = {
    --     "ansiblels",
    --     "bashls",
    --     "cssls",
    --     "html",
    --     "lua_ls",
    --     "pyright",
    --     "tsserver"
    --   },
    --   -- auto-install configured servers (with lspconfig)
    --   automatic_installation = true,
    -- }

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
        "xmlformatter",
        "yamlfmt",
      },
      -- auto-install configured servers (with lspconfig)
      automatic_installation = true,
    }

    -- vim.api.nvim_create_autocmd('User', {
    --   pattern = 'MasonToolsStartingInstall',
    --   callback = function()
    --     vim.schedule(function()
    --       print 'mason-tool-installer is starting'
    --     end)
    --   end,
    -- })

    -- custom nvchad cmd to install all mason binaries listed
    -- https://github.com/NvChad/NvChad
    -- vim.api.nvim_create_user_command("MasonInstallAll", function()
    --   vim.cmd("MasonInstall")
    --   vim.cmd('MasonToolsInstall')
    -- end, {})

    -- vim.g.mason_binaries_list = ensure_installed
  end,
}

return plugins
