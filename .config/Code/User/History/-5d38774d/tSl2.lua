-- configure lsp servers
local configs = require("plugins.configs.lspconfig")
local lspconfig = require("lspconfig")

vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(vim.lsp.diagnostic.on_publish_diagnostics, {
    underline = false,
    update_in_insert = false,
    virtual_text = { spacing = 4, prefix = "●" },
    severity_sort = true,
})

vim.cmd [[highlight DiagnosticUnderlineError cterm=undercurl gui=undercurl guisp=Red]]

local servers = {
    "ansiblels",
    "bashls",
    "cssls",
    "html",
    "lua_ls",
    "pyright",
    "tsserver",
}

for _, lsp in ipairs(servers) do
    lspconfig[lsp].setup {
        on_attach = configs.on_attach,
        capabilities = configs.capabilities,
    }
end
