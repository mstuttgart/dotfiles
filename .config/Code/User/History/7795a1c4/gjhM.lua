-- configure LSP
local plugins = {
    'neovim/nvim-lspconfig',
    dependencies = {
        -- LSP Support
        'williamboman/mason.nvim',
        'williamboman/mason-lspconfig.nvim',

        -- Autocompletion
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
        -- local lsp = require('lsp-zero').preset {}

        -- lsp.on_attach(function(client, bufnr)
        --     lsp.default_keymaps { buffer = bufnr }
        --     lsp.buffer_autoformat()
        -- end)

        -- lsp.set_sign_icons {
        --     error = '✘',
        --     warn = '▲',
        --     hint = '⚑',
        --     info = '»',
        -- }

        -- lsp.ensure_installed {
        --     'pyright',
        --     'html',
        --     'cssls',
        --     'lua_ls',
        --     'bashls',
        --     'ansiblels',
        -- }

        require('mason-lspconfig').setup({
            ensure_installed = {},
            handlers = {
                lsp_zero.default_setup,
            },
        })

        -- configure language servers
        require('lspconfig').lua_ls.setup({})
        require('lspconfig').pyright.setup({})
        require('lspconfig').bashls.setup({})

        lsp.setup()
    end,
}

return plugins
