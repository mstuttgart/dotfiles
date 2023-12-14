-- settings terminal

local plugin = {
    'CRAG666/betterTerm.nvim',
    config = function()
        require('betterTerm').setup {}
    end,
    init = function()
        vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = '[S]earch [F]iles' })
        vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = '[S]earch current [W]ord' })
        vim.keymap.set('n', '<leader>sg', require('telescope').extensions.live_grep_args.live_grep_args, { desc = '[S]earch by [G]rep' })
    end
}

return plugin
