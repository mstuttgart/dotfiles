-- lsp config
local status_lsp, lsp = pcall(require, 'lspconfig')
local status_mason, mason = pcall(require, 'mason')
local status_masoncfg, masoncfg = pcall(require, 'mason-lspconfig')

if (not status_lsp or not status_mason or not status_masoncfg) then return end

mason.setup()

masoncfg.setup({
  ensure_installed = { 'lua_ls', 'pyright', 'yamlls', 'eslint' }
})

local augroup_format = vim.api.nvim_create_augroup("Format", { clear = true })

local enable_format_on_save = function(_, bufnr)
  vim.api.nvim_clear_autocmds({ group = augroup_format, buffer = bufnr })
  vim.api.nvim_create_autocmd("BufWritePre", {
    group = augroup_format,
    buffer = bufnr,
    callback = function()
      vim.lsp.buf.format({ bufnr = bufnr })
    end,
  })
end

local capabilities = require('cmp_nvim_lsp').default_capabilities()

-- lua server
lsp.lua_ls.setup {
  capabilities = capabilities,
  on_attach = function(client, bufnr)
    on_attach(client, bufnr)
    enable_format_on_save(client, bufnr)
    require("nvim-navic").attach(client, bufnr)
  end,
  settings = {
    Lua = {
      diagnostics = {
        -- Get the language server to recognize the `vim` and 'use' global
        globals = { 'vim', 'use' },
      },

      workspace = {
        -- Make the server aware of Neovim runtime files
        library = vim.api.nvim_get_runtime_file("", true),
        checkThirdParty = false
      },
    },
  },
}

-- python server
lsp.pyright.setup{
  capabilities = capabilities
}

-- yaml server
lsp.yamlls.setup{
  capabilities = capabilities
}

-- javascript server
lsp.eslint.setup{
  capabilities = capabilities
}

-- Use LspAttach autocommand to only map the following keys
-- after the language server attaches to the current buffer
vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('UserLspConfig', {}),
  callback = function(ev)
    -- Enable completion triggered by <c-x><c-o>
    -- vim.bo[ev.buf].omnifunc = 'v:lua.vim.lsp.omnifunc'

    -- Buffer local mappings.
    -- See `:help vim.lsp.*` for documentation on any of the below functions
    local opts = { noremap = true, silent = true }

    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, opts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, opts)
    vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, opts)

  end,
})
