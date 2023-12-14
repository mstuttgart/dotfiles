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
        end
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

    -- navic complement to breadcumbs
    {
        'utilyre/barbecue.nvim',
        version = '*',
        dependencies = {
            'SmiteshP/nvim-navic',
            'nvim-tree/nvim-web-devicons',
        },
        config = true,
    },

    -- smooth scroll
    {
        "karb94/neoscroll.nvim",
        config = function()
            require('neoscroll').setup {}
        end
    },

}

return plugins
