local configs = require("plugins.configs.lspconfig")
local capabilities = configs.capabilities

local on_attach = configs.on_attach

local lspconfig = require("lspconfig")

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
        on_attach = on_attach,
        capabilities = capabilities,
    }
end
