-- bufferline settiplit
-- gs

local plugin = {
    'akinsho/bufferline.nvim',
    dependencies = {
        { 'echasnovski/mini.bufremove', version = '*' },
    },
    event = 'VeryLazy',
    keys = {
        { '<leader>bQ', '<Cmd>BufferLineGroupClose ungrouped<CR>', desc = 'Delete all buffers' },
        { '<leader>bb', '<Cmd>BufferLineCycleNext<CR>', desc = 'Next Buffer' },
        { '<lkeader>bp', '<Cmd>BufferLineCyclePrev<CR>', desc = 'Previous Buffers' },
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
            separator_style = 'thin',
            always_show_bufferline = true,
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
