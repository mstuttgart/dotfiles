-- mini surround settings

-- surround chars autocomplete
local plugin = {
    'echasnovski/mini.surround',
    config = function ()
        require('mini.surround').setup()
    end,
    opts = {
        mappings = {
            add = "gsa",
            delete = "gsd",
            find = "gsf",
            find_left = "gsF",
            highlight = "gsh",
            replace = "gsr",
            update_n_lines = "gsn",
          },
    },
}

return plugin
