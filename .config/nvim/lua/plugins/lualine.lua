-- lualine settings

local plugin = {
    'nvim-lualine/lualine.nvim',
    dependencies = {
        'nvim-tree/nvim-tree.lua',
    },
    event = 'VeryLazy',
    opts = function()
        return {
            options = {
                theme = 'auto',
                globalstatus = true,
                disabled_filetypes = { statusline = { 'dashboard', 'alpha' } },
            },
            sections = {
                lualine_a = { 'mode' },
                lualine_b = { 'branch' },
                lualine_c = {
                    {
                        'diagnostics',
                        error = ' ',
                        warn = ' ',
                        info = ' ',
                        hint = ' ',
                    },
                    {
                        'filetype',
                        icon_only = true,
                        separator = '',
                        padding = {
                            left = 1,
                            right = 0,
                        },
                    },
                    {
                        'filename',
                        path = 1,
                        symbols = { modified = '  ', readonly = '', unnamed = '' },
                    },
                },
                lualine_x = {
                    -- stylua: ignore
                    {
                        function() return require('noice').api.status.command.get() end,
                        cond = function() return package.loaded['noice'] and require('noice').api.status.command.has() end,
                    },
                    -- stylua: ignore
                    {
                        function() return require('noice').api.status.mode.get() end,
                        cond = function() return package.loaded['noice'] and require('noice').api.status.mode.has() end,
                    },
                },
                lualine_y = {
                    { 'progress', separator = ' ', padding = { left = 1, right = 0 } },
                    { 'location', padding = { left = 0, right = 1 } },
                },
                lualine_z = {
                    function()
                        return ' ' .. os.date('%R')
                    end,
                },
            },
            extensions = { 'nvim-tree', 'lazy' },
        }
    end,
}

return plugin
