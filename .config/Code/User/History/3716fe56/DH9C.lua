-- configure 'plug-n-play' plugins

local plugins = {

    -- auto close chars like '(', '{', '[' and ''
    {
        'windwp/nvim-autopairs',
        config = true,
    },

    -- csv highlight
    {
        'mechatroner/rainbow_csv',
    },

    -- highlight for color code
    {
        'norcalli/nvim-colorizer.lua',
        config = function()
            require('colorizer').setup(nil, { css = true })
        end,
    },

    -- Useful plugin to show you pending keybinds.
    {
        'folke/which-key.nvim',
        event = "VeryLazy",
        init = function()
            vim.o.timeout = true
            vim.o.timeoutlen = 300
        end,
        config = function()
            require('which-key').setup()
        end,
    },

    {
        'stevearc/aerial.nvim',
        opts = {},
        -- Optional dependencies
        dependencies = {
            "nvim-treesitter/nvim-treesitter",
            "nvim-tree/nvim-web-devicons"
        },
    },

    -- bradcumbs
    {
        'Bekaboo/dropbar.nvim',
        -- optional, but required for fuzzy finder support
        dependencies = {
            'nvim-telescope/telescope-fzf-native.nvim',
            'nvim-tree/nvim-web-devicons',

        }
    },

    -- smooth scroll
    {
        "karb94/neoscroll.nvim",
        config = function()
            require('neoscroll').setup {}
        end
    },

    -- better vim.ui
    {
        'stevearc/dressing.nvim',
        opts = {},
        event = 'VeryLazy',
    },

}

return plugins
