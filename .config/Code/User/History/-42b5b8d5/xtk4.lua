-- A better annotation generator.
local plugin = {
    "danymat/neogen",
    event = "VeryLazy",
    dependencies = "nvim-treesitter/nvim-treesitter",
    config = true,
    init = function()
        vim.keymap.set("n", "<leader>cd", ':lua require("neogen").generate()<CR>',
            { silent = true, desc = "Generate Documentation" }
        )
    end,
}

return plugin
