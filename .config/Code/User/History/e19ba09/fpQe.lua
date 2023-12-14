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
        priority=1000,
        lazy = false,
    },
    -- {
    --     'maxmx03/solarized.nvim',
    --     priority=1000,
    --     lazy = true,
    --     config = function()
    --         -- vim.o.background = 'dark' -- or 'light'
    --         -- vim.cmd.colorscheme 'solarized'
    --     end,
    -- },
}

return plugins
