-- configure LSP
local plugins = {
  "neovim/nvim-lspconfig",
  event = { "BufReadPre", "BufNewFile" },
  dependencies = {
    -- Autocompletion
    "williamboman/mason-lspconfig.nvim", -- need to install before
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    local lspconfig = require "lspconfig"
    -- import cmp-nvim-lsp plugin
    local cmp_nvim_lsp = require "cmp_nvim_lsp"

    -- local capabilities = vim.lsp.protocol.make_client_capabilities()
    local capabilities = cmp_nvim_lsp.default_capabilities()

    -- for _, server_name in ipairs(servers) do
    --   lspconfig[server_name].setup {
    --     capabilities = capabilities,
    --     on_attach = on_attach,
    --   }
    -- end

    lspconfig['pyright'].setup {
      capabilities = capabilities,
    }

    lspconfig['bashls'].setup {
      capabilities = capabilities,
    }

    -- configure lua server (with special settings)
    lspconfig["lua_ls"].setup {
      capabilities = capabilities,
      on_attach = on_attach,
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
