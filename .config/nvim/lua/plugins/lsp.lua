-- lsp settings
--
local plugin = {
    {
        'VonHeikemen/lsp-zero.nvim',
        branch = 'v2.x',
        dependencies = {
            -- LSP Support
            { 'neovim/nvim-lspconfig' }, -- Required
            { -- Optional
                'williamboman/mason.nvim',
                build = function()
                    pcall(vim.cmd, 'MasonUpdate')
                end,
            },
            { 'williamboman/mason-lspconfig.nvim' }, -- Optional
            'folke/neodev.nvim',

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

            -- complements
            'onsails/lspkind-nvim', -- add the nice source + completion item kind to the menu
        },
        init = function()
            require('mason').setup {
                ui = {
                    border = 'rounded',
                },
            }
            local lsp = require('lsp-zero').preset {}

            lsp.on_attach(function(client, bufnr)
                lsp.default_keymaps { buffer = bufnr }
                lsp.buffer_autoformat()
            end)

            lsp.set_sign_icons {
                error = '✘',
                warn = '▲',
                hint = '⚑',
                info = '»',
            }

            lsp.ensure_installed {
                -- Replace these with whatever servers you want to install
                'pyright',
                'yamlls',
                'html',
                'cssls',
            }

            -- (Optional) Configure lua language server for neovim
            require('lspconfig').lua_ls.setup(lsp.nvim_lua_ls())

            lsp.setup()
        end,
    },
}

return plugin
