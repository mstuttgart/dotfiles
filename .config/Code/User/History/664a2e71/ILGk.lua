-- lsp settings
--
local plugin = {
    'neovim/nvim-lspconfig',
    dependencies = {
        {
            'williamboman/mason.nvim',
            build = function()
                pcall(vim.cmd, 'MasonUpdate')
            end,
        },
        'williamboman/mason-lspconfig.nvim',
        "WhoIsSethDaniel/mason-tool-installer.nvim",
    },
    init = function()

        require('mason').setup({
            ui = {
                icons = {
                    package_installed = "✓",
                    package_pending = "➜",
                    package_uninstalled = "✗",
                },
            },
        })
        
        require('mason-lspconfig').setup({
            ensure_installed = {
                'pyright',
                'yamlls',
                'html',
                'cssls',
                'lua_ls',
                'bashls',
                'ansiblels',
            }
        })

        local capabilities = vim.lsp.protocol.make_client_capabilities()
        capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

        local lspconfig = require('lspconfig')
        local get_servers = require('mason-lspconfig').get_installed_servers

        for _, server_name in ipairs(get_servers()) do
            lspconfig[server_name].setup({
                
            })
        end
    end,
}

return plugin
