-- lualine settings

local M = {
    'nvim-lualine/lualine.nvim',
    dependencies = {
        'nvim-tree/nvim-tree.lua',
    },
    event = 'VeryLazy',
}

function M.config()

    require('lualine')


end

return M



local plugin = {
    'nvim-lualine/lualine.nvim',
    dependencies = {
        'nvim-tree/nvim-tree.lua',
    },
    event = 'VeryLazy',
    opts = function()
        return {

        }
    end,
}

return plugin
 