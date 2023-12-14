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
  config = function()
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
      ensure_installed = servers,
    }

    local lspconfig = require "lspconfig"

    -- configure language servers
    -- lspconfig.ansiblels.setup({})
    -- lspconfig.bashls.setup {}
    -- lspconfig.cssls.setup({})
    -- lspconfig.html.setup({})
    -- lspconfig.lua_ls.setup({})
        -- lspconfig.pyright.setup({})
    
        local keymap = vim.keymap -- for conciseness

        local opts = { noremap = true, silent = true }
    
    local on_attach = function(client, bufnr)
      opts.buffer = bufnr

      -- set keybinds
      opts.desc = "Show LSP references"
      keymap.set("n", "gR", "<cmd>Telescope lsp_references<CR>", opts) -- show definition, references

      opts.desc = "Go to declaration"
      keymap.set("n", "gD", vim.lsp.buf.declaration, opts) -- go to declaration

      opts.desc = "Show LSP definitions"
      keymap.set("n", "gd", "<cmd>Telescope lsp_definitions<CR>", opts) -- show lsp definitions

      opts.desc = "Show LSP implementations"
      keymap.set("n", "gi", "<cmd>Telescope lsp_implementations<CR>", opts) -- show lsp implementations

      opts.desc = "Show LSP type definitions"
      keymap.set("n", "gt", "<cmd>Telescope lsp_type_definitions<CR>", opts) -- show lsp type definitions

      opts.desc = "See available code actions"
      keymap.set({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, opts) -- see available code actions, in visual mode will apply to selection

      opts.desc = "Smart rename"
      keymap.set("n", "<leader>rn", vim.lsp.buf.rename, opts) -- smart rename

      opts.desc = "Show buffer diagnostics"
      keymap.set("n", "<leader>D", "<cmd>Telescope diagnostics bufnr=0<CR>", opts) -- show  diagnostics for file

      opts.desc = "Show line diagnostics"
      keymap.set("n", "<leader>d", vim.diagnostic.open_float, opts) -- show diagnostics for line

      opts.desc = "Go to previous diagnostic"
      keymap.set("n", "[d", vim.diagnostic.goto_prev, opts) -- jump to previous diagnostic in buffer

      opts.desc = "Go to next diagnostic"
      keymap.set("n", "]d", vim.diagnostic.goto_next, opts) -- jump to next diagnostic in buffer

      opts.desc = "Show documentation for what is under cursor"
      keymap.set("n", "K", vim.lsp.buf.hover, opts) -- show documentation for what is under cursor

      opts.desc = "Restart LSP"
      keymap.set("n", "<leader>rs", ":LspRestart<CR>", opts) -- mapping to restart lsp if necessary
    end

    local capabilities = vim.lsp.protocol.make_client_capabilities()
    -- local capabilities = require("cmp_nvim_lsp").default_capabilities()

    -- local get_servers = require("mason-lspconfig").get_installed_servers

    for _, server_name in ipairs(servers) do
      lspconfig[server_name].setup {
        capabilities = capabilities,
      }
    end

    -- lspconfig["bashls"].setup {
    --   capabilities = capabilities,
    -- }
  end,
}

return plugins
