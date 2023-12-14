-- lsp settings
--
local plugin = {
    'VonHeikemen/lsp-zero.nvim',
    branch = 'v2.x',
    dependencies = {
        -- LSP Support
        { 'neovim/nvim-lspconfig' },
        {
            'williamboman/mason.nvim',
            build = function()
                pcall(vim.cmd, 'MasonUpdate')
            end,
        },
        'williamboman/mason-lspconfig.nvim',
        -- Autocompletion
        -- completion sources
        'hrsh7th/cmp-nvim-lsp',
        'hrsh7th/cmp-nvim-lua',
        'hrsh7th/cmp-buffer',
        'hrsh7th/cmp-cmdline',
        'hrsh7th/nvim-cmp',
        'hrsh7th/cmp-path',
        'saadparwaiz1/cmp_luasnip',
        'L3MON4D3/LuaSnip',
        'rafamadriz/friendly-snippets',
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

        local lsp = require('lsp-zero').preset {}

        lsp.on_attach(function(client, bufnr)
            lsp.default_keymaps { buffer = bufnr }
            -- lsp.buffer_autoformat()
        end)

        lsp.set_sign_icons {
            error = '✘',
            warn = '▲',
            hint = '⚑',
            info = '»',
        }

        -- (Optional) Configure lua language server for neovim
        require('lspconfig').lua_ls.setup(lsp.nvim_lua_ls())

        local capabilities = vim.lsp.protocol.make_client_capabilities()
        capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

        local lspconfig = require('lspconfig')
        local get_servers = require('mason-lspconfig').get_installed_servers

        for _, server_name in ipairs(get_servers()) do
            lspconfig[server_name].setup({
                capabilities = capabilities,
            })
        end
    end,
}

return plugin
