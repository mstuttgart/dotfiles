-- neogen settings

local plugin = {
    'danymat/neogen',
    config = true,
    init = function()
        vim.keymap.set(
            'n',
            '<Leader>ca',
            ':lua require("neogen").generate()<CR>',
            { silent = true, desc = 'Add [C]ode [A]nnotation ' }
        )
    end,
}

return plugin
