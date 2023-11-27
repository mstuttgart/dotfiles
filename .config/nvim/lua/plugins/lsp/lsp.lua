-- configure LSP
local plugins = {
  "neovim/nvim-lspconfig",
  event = { "BufReadPre", "BufNewFile" },
  dependencies = {
    "williamboman/mason-lspconfig.nvim",
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    local lspconfig = require "lspconfig"

    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities = require("cmp_nvim_lsp").default_capabilities(capabilities)

    local get_servers = require("mason-lspconfig").get_installed_servers

    -- vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(vim.lsp.diagnostic.on_publish_diagnostics, {
    --   underline = true,
    --   update_in_insert = false,
    --   virtual_text = { spacing = 4, prefix = "●" },
    --   severity_sort = true,
    -- })

    for _, server_name in ipairs(get_servers()) do
      lspconfig[server_name].setup {
        capabilities = capabilities,
      }
    end

    -- configure javascript and typescript
    -- lspconfig["tsserver"].setup {
    --   filetypes = { "javascript", "typescript", "typescriptreact", "typescript.tsx" },
    --   root_dir = function() return vim.loop.cwd() end
    -- }

    -- configure lua server (with special settings)
    lspconfig["lua_ls"].setup {
      capabilities = capabilities,
      settings = { -- custom settings for lua
        Lua = {
          -- make the language server recognize "vim" global
          diagnostics = {
            globals = { "vim" },
          },
          workspace = {
            -- make language server aware of runtime files
            library = {
              [vim.fn.expand "$VIMRUNTIME/lua"] = true,
              [vim.fn.stdpath "config" .. "/lua"] = true,
            },
          },
        },
      },
    }
  end,
}

return plugins
