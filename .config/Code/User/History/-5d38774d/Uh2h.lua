-- configure lsp servers
local configs = require("plugins.configs.lspconfig")
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
        on_attach = configs.on_attach,
        capabilities = configs.capabilities,
    }
end
