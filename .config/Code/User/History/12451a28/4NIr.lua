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
-- }


-- local plugin = {
--     'kessejones/term.nvim',
--     config = function()
--         require('term').setup {}
--     end,
--     init = function()
--         vim.keymap.set({ 't' }, '<C-p>', require('term').new, { silent = true })
--         vim.keymap.set({ 'n', 't' }, '<leader>;', require('term').toggle, { silent = true })
--         vim.keymap.set({ 't' }, '<C-n>', require('term').next, { silent = true })
--         vim.keymap.set({ 't' }, '<C-p>', require('term').prev, { silent = true })
--     end
-- }

local plugin = {
    "NvChad/nvterm",
    config = function()
        require("nvterm").setup()
    end,
    init = function()
        -- vim.keymap.set({ 't' }, '<C-p>', require('nvterm').new, { silent = true })
        vim.keymap.set({ 'n', 't' }, '<leader>;', function () require('nvterm').toggle('horizontal') end, { silent = true })
        -- vim.keymap.set({ 't' }, '<C-n>', require('nvterm').next, { silent = true })
    end
}

return plugin
