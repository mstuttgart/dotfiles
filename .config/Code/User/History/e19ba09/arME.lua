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
        lazy = true,
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
        "craftzdog/solarized-osaka.nvim",
        lazy = false,
        priority = 1000,
        opts = {},
      }
}

return plugins
