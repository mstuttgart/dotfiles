-- configure LSP
local plugins = {
  "neovim/nvim-lspconfig",
  dependencies = {
    -- LSP Support
    "williamboman/mason.nvim",
    "williamboman/mason-lspconfig.nvim",

    -- Autocompletion
    "hrsh7th/cmp-nvim-lsp",
    "hrsh7th/cmp-nvim-lua",
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-cmdline",
    "hrsh7th/nvim-cmp",
    "hrsh7th/cmp-path",
    "saadparwaiz1/cmp_luasnip",

    -- snippets engine
    "L3MON4D3/LuaSnip",

    -- snippets collection
    "rafamadriz/friendly-snippets",

    -- complements
    "onsails/lspkind-nvim", -- add the nice source + completion item kind to the menu
  },
    copfig = function()
    
    require("mason").setup {
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗",
        },
      },
    }

    local servers = {
      "pyright",
      "html",
      "cssls",
      "lua_ls",
      "bashls",
      "ansiblels",
    }

    -- auto install LSP
    require("mason-lspconfig").setup {
      ensure_installed = servers
    }

    local lspconfig = require "lspconfig"

    -- configure language servers
    -- lspconfig.ansiblels.setup({})
    -- lspconfig.bashls.setup {}
    -- lspconfig.cssls.setup({})
    -- lspconfig.html.setup({})
    -- lspconfig.lua_ls.setup({})
    -- lspconfig.pyright.setup({})

    local capabilities = vim.lsp.protocol.make_client_capabilities()
    -- local capabilities = require("cmp_nvim_lsp").default_capabilities()

    local get_servers = require("mason-lspconfig").get_installed_servers

    for _, server_name in ipairs(get_servers()) do
      lspconfig[server_name].setup {
        capabilities = capabilities,
      }
    end

    lspconfig["bashls"].setup {
      capabilities = capabilities,
    }
  end,
}

return plugins
