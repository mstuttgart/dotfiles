-- settings terminal

local plugin = {
    "NvChad/nvterm",
    config = function()
        require("nvterm").setup()
    end,
    init = function()
        -- vim.keymap.set({ 't' }, '<C-p>', require('nvterm').new, { silent = true })
        vim.keymap.set({ 'n', 't' }, '<leader>;', function () require("nvterm.terminal").toggle('horizontal') end, { silent = true })
        -- vim.keymap.set({ 't' }, '<C-n>', require('nvterm').next, { silent = true })
    end
}

return plugin
