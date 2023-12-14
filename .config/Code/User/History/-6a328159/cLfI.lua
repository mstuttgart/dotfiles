-- mini surround settings

-- surround chars autocomplete
local plugin = {
    'echasnovski/mini.surround',
    config = function ()
        require('mini.surround').setup()
    end,
    opts = {
        mappings = {
            add = 'gsa', -- Add surrounding in Normal and Visual modes
            delete = 'gsd', -- Delete surrounding
            find = 'gsf', -- Find surrounding (to the right)
            find_left = 'gsF', -- Find surrounding (to the left)
            highlight = 'g', -- Highlight surrounding
            replace = 'gzr', -- Replace surrounding
            update_n_lines = 'gzn', -- Update `n_lines`
        },
    },
}

return plugin
