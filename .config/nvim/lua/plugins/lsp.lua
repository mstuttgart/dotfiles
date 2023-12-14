-- configure LSP
local plugins = {
  "neovim/nvim-lspconfig",
  event = { "BufReadPre", "BufNewFile" },
  dependencies = {
    "WhoIsSethDaniel/mason-tool-installer.nvim",
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    local lspconfig = require "lspconfig"

    local capabilities = vim.lsp.protocol.make_client_capabilities()
    capabilities = require("cmp_nvim_lsp").default_capabilities(capabilities)

    -- local get_servers = require("mason-lspconfig").get_installed_servers

    vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(vim.lsp.diagnostic.on_publish_diagnostics, {
      undercurl = true,
      update_in_insert = false,
      virtual_text = { spacing = 4, prefix = "●" },
      severity_sort = true,
    })

    vim.cmd [[highlight DiagnosticUnderlineError cterm=undercurl gui=undercurl guisp=undercurl]]

    -- for _, server_name in ipairs(get_servers()) do
    --   lspconfig[server_name].setup {
    --     capabilities = capabilities,
    --   }
    -- end

    -- configure html server
    lspconfig["html"].setup {
      capabilities = capabilities,
    }

    -- configure typescript server with plugin
    lspconfig["tsserver"].setup {
      capabilities = capabilities,
    }

    -- configure css server
    lspconfig["cssls"].setup {
      capabilities = capabilities,
    }

    -- configure python server
    lspconfig["pyright"].setup {
      capabilities = capabilities,
    }

    -- configure bash server
    lspconfig["bashls"].setup {
      capabilities = capabilities,
    }

    -- configure ansible server
    lspconfig["ansiblels"].setup {
      capabilities = capabilities,
    }

    -- configure lua server
    lspconfig["lua_ls"].setup {
      capabilities = capabilities,
    }

    -- configure lua server (with special settings)
    -- lspconfig["lua_ls"].setup {
    --   capabilities = capabilities,
    --   settings = { -- custom settings for lua
    --     Lua = {
    --       -- make the language server recognize "vim" global
    --       diagnostics = {
    --         globals = { "vim" },
    --       },
    --       workspace = {
    --         -- make language server aware of runtime files
    --         library = {
    --           [vim.fn.expand "$VIMRUNTIME/lua"] = true,
    --           [vim.fn.stdpath "config" .. "/lua"] = true,
    --         },
    --       },
    --     },
    --   },
    -- }
  end,
}

return plugins
