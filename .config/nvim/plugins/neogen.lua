-- neogen settings

local plugin = {
    'danymat/neogen',
    config = true,
    init = function()
        vim.keymap.set(
            'n',
            '<Leader>gd',
            ':lua require("neogen").generate()<CR>',
            { silent = true, desc = 'Generate Documentation' }
        )
    end,
}

return plugin
