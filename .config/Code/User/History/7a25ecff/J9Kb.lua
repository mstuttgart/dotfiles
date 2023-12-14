-- Configure mason to autoinstall linters and formatters
local plugins = {
  "williamboman/mason.nvim",
  cmd = { "Mason", "MasonInstall", "MasonInstallAll", "MasonUpdate" },
  -- dependencies = {
  --   "williamboman/mason-lspconfig.nvim",
  --   "WhoIsSethDaniel/mason-tool-installer.nvim",
  -- },
  opts = {
    -- ensure_installed = {
    --         "lua-language-server",
    -- },
    PATH = "skip",
    ui = {
      icons = {
        package_installed = "✓",
        package_pending = "➜",
        package_uninstalled = "✗",
      },
    },
  },
  config = function(_, opts)
    require("mason").setup(opts)
    -- onverride mason icons
    -- require("mason").setup {
    --   ui = {
    --     icons = {
    --       package_installed = "✓",
    --       package_pending = "➜",
    --       package_uninstalled = "✗",
    --     },
    --   },
    -- }

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
    }

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

    -- require("mason-tool-installer").setup {
    --   ensure_installed = {
    --     -- linters
    --     "eslint_d",
    --     "pylint",
    --     "shellcheck",

    --     -- formatters
    --     "autopep8",
    --     "isort",
    --     "prettier",
    --     "shfmt",
    --     "stylua",
    --     "xmlformatter",
    --     "yamlfmt",
    --   },
    -- }

    -- custom nvchad cmd to install all mason binaries listed
    vim.api.nvim_create_user_command("MasonInstallAll", function()
      vim.cmd("MasonInstall " .. table.concat(ensure_installed, " "))
    end, {})

    vim.g.mason_binaries_list = ensure_installed
  end,
}

return plugins
