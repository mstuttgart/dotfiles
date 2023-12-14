-- A better annotation generator.
local plugin = {
    "danymat/neogen",
    config = true,
    event = "VeryLazy",
    init = function()
        vim.keymap.set("n", "<Leader>cd", ':lua require("neogen").generate()<CR>',
            { silent = true, desc = "Generate Documentation" }
        )
    end,
}

return plugin
