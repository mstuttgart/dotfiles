-- bufferline settiplit
-- gs

local plugin = {
    'akinsho/bufferline.nvim',
    dependencies = {
        { 'echasnovski/mini.bufremove', version = '*' },
    },
    event = 'VeryLazy',
    keys = {
        { '<leader>bp', '<Cmd>BufferLineTogglePin<CR>', desc = 'Toggle pin' },
        { '<leader>bQ', '<Cmd>BufferLineGroupClose ungrouped<CR>', desc = 'Delete all buffers' },
    },
    opts = {
        options = {
            close_command = function(n)
                require('mini.bufremove').delete(n, false)
            end,
            right_mouse_command = function(n)
                require('mini.bufremove').delete(n, false)
            end,
            diagnostics = 'nvim_lsp',
            separator_style = 'slant',
            always_show_bufferline = true,
            diagnostics_indicator = function(count, level, diagnostics_dict, context)
                local icon = level:match('error') and ' ' or ' '
                return ' ' .. icon .. count
            end,
            offsets = {
                {
                    filetype = 'NvimTree',
                    text = '',
                    highlight = 'Directory',
                    text_align = 'left',
                    separator = false,
                },
            },
        },
    },
}

return plugin
