-- telescope settings

-- Fuzzy Finder (files, lsp, etc)
local plugin = {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
        'nvim-lua/plenary.nvim',
        'stevearc/aerial.nvim',
        {
            'nvim-telescope/telescope-fzf-native.nvim',
            build = 'make',
        },
        {
            'nvim-telescope/telescope-live-grep-args.nvim',
        },
    },
    config = function()
        require('telescope').load_extension('fzf')
        require('telescope').load_extension('live_grep_args')
        require("telescope").load_extension("aerial")
    end,
    init = function()
        vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = '[S]earch [F]iles' })
        vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = '[S]earch current [W]ord' })
        vim.keymap.set('n', '<leader>sg', require('telescope').extensions.live_grep_args.live_grep_args, { desc = '[S]earch by [G]rep' })
        vim.keymap.set('n', '<leader>sa', require("telescope").extensions.aerial.aerial, { desc = '[S]earch by Aerial' })
    end,
}

return plugin