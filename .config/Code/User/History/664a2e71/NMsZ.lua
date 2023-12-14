-- lsp settings
--
local plugin = {
    'neovim/nvim-lspconfig',
    dependencies = {
        -- LSP Support
        -- { 'neovim/nvim-lspconfig' }, -- Required
        { -- Optional
            'williamboman/mason.nvim',
            build = function()
                pcall(vim.cmd, 'MasonUpdate')
            end,
        },
        { 'williamboman/mason-lspconfig.nvim' }, -- Optional
    },
    init = function()
        require('mason').setup()
        require('mason-lspconfig').setup({
            ensure_installed = {
                -- Replace these with whatever servers you want to install
                'pyright',
                'yamlls',
                'htmlls',
                'cssls',
                'lua_ls',
                'bashls',
                'ansiblels',
            }
        })

        -- local lsp = require('lsp-zero').preset {}

        -- lsp.on_attach(function(client, bufnr)
        --     lsp.default_keymaps { buffer = bufnr }
        -- end)

        -- lsp.set_sign_icons {
        --     error = '✘',
        --     warn = '▲',
        --     hint = '⚑',
        --     info = '»',
        -- }

        -- lsp.ensure_installed {
        --     -- Replace these with whatever servers you want to install
        --     'pyright',
        --     'yamlls',
        --     'htmlls',
        --     'cssls',
        --     'lua_ls',
        --     'bashls',
        --     'ansiblels',
        -- }

        -- -- (Optional) Configure lua language server for neovim
        -- require('lspconfig').lua_ls.setup(lsp.nvim_lua_ls())
        -- require('lspconfig').pyright.setup {}

        local lspconfig = require('lspconfig')
        local get_servers = require('mason-lspconfig').get_installed_servers

        for _, server_name in ipairs(get_servers()) do
            lspconfig[server_name].setup({
                capabilities = lsp_capabilities,
            })
        end

        lsp.setup()
    end,
}

return plugin
