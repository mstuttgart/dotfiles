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
        lazy = false,
    },
    {
        'maxmx03/solarized.nvim',
        lazy = true,
        config = function()
            vim.o.background = 'dark' -- or 'light'
            vim.cmd.colorscheme 'solarized'
        end,
    },
}

return plugins
