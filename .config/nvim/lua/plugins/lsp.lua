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
        { 'williamboman/mason-lspconfig.nvim' },
    },
    init = function()
        require('mason').setup()
        require('mason-lspconfig').setup({
            ensure_installed = {
                'pyright',
                'yamlls',
                'htmlls',
                'cssls',
                'lua_ls',
                'bashls',
                'ansiblels',
            }
        })

        local lspconfig = require('lspconfig')
        local get_servers = require('mason-lspconfig').get_installed_servers

        for _, server_name in ipairs(get_servers()) do
            lspconfig[server_name].setup({})
        end

    end,
}

return plugin
