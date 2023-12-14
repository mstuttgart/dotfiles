-- A better annotation generator.
local plugin = {
    "danymat/neogen",
    event = "VeryLazy",
    dependencies = "nvim-treesitter/nvim-treesitter",
    config = function ()
        
    end,
    init = function()
        local opts = { noremap = true, silent = true }

        vim.api.nvim_set_keymap("i", "<C-l>", ":lua require('neogen').jump_next<CR>", opts)
        vim.api.nvim_set_keymap("i", "<C-h>", ":lua require('neogen').jump_prev<CR>", opts)

        vim.keymap.set("n", "<leader>cd", ':lua require("neogen").generate()<CR>',
            { silent = true, desc = "Generate Documentation" }
        )
    end,
}

return plugin
