-- colorschemes

local plugins = {
    {
        'Shatur/neovim-ayu',
        lazy = true,
    },
    {
        'folke/tokyonight.nvim',
        lazy = true,
        opts = {
            style = 'moon',
        },
    },
    {
        'navarasu/onedark.nvim',
        lazy = true,
    },
    {
        'sainnhe/everforest',
        lazy = false,
        config = function()
            require('everforest').setup {
                -- background = 'medium',
                -- transparent_background_level = 1,
                -- italics = true,
                -- disable_italic_comments = false,
                -- ui_contrast = 'low',
            }
        end,
    },
    {
        'maxmx03/solarized.nvim',
        lazy = true,
        -- priority = 1000,
        config = function()
            vim.o.background = 'dark' -- or 'light'

            vim.cmd.colorscheme 'solarized'
        end,
    },
}

return plugins
