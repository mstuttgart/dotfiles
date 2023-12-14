-- configure 'plug-n-play' plugins

return {

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
        opts = {},
        lazy = true,
    },

    {
        "williamboman/mason.nvim",
        build = ":MasonUpdate",
        cmd = { "Mason", "MasonInstall" },
        config = function()
            require("mason").setup()
        end,
    },

    -- - navic complement to breadcumbs
    -- {
    --     'utilyre/barbecue.nvim',
    --     version = '*',
    --     dependencies = {
    --         'SmiteshP/nvim-navic',
    --         'nvim-tree/nvim-web-devicons',
    --     },
    --     config = true,
    -- },

    -- better vim.ui
    -- {
    --     'stevearc/dressing.nvim',
    --     opts = {},
    --     event = 'VeryLazy',
    -- },

}
