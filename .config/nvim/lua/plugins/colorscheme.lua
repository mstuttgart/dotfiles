-- colorschemes

local plugins = {
    {
        'Shatur/neovim-ayu',
        lazy = true,
    },
    {
        'navarasu/onedark.nvim',
        lazy = true,
    },
    {
        'sainnhe/everforest',
        priority = 1000,
        config = function()
            vim.cmd([[colorscheme everforest]])
        end,
    },
}

return plugins
