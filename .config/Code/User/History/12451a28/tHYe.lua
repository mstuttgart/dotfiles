-- settings terminal

-- local plugin = {
--     'CRAG666/betterTerm.nvim',
--     config = function()
--         require('betterTerm').setup {}
--     end,
--     init = function()
--         local betterTerm = require('betterTerm')
--         -- toggle firts term
--         vim.keymap.set({ "n", "t" }, "<C-;>", betterTerm.open, { desc = "Open terminal" })
--         -- Select term focus
--         vim.keymap.set({ "n" }, "<leader>tt", betterTerm.select, { desc = "Select terminal" })
--     end
}


local plugin = {
    'CRAG666/betterTerm.nvim',
    config = function()
        require('betterTerm').setup {}
    end,
    init = function()
        local betterTerm = require('betterTerm')
        -- toggle firts term
        vim.keymap.set({ "n", "t" }, "<C-;>", betterTerm.open, { desc = "Open terminal" })
        -- Select term focus
        vim.keymap.set({ "n" }, "<leader>tt", betterTerm.select, { desc = "Select terminal" })
    end
}

return plugin
