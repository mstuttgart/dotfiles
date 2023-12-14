-- telescope settings

-- Fuzzy Finder (files, lsp, etc)
local plugin = {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
        'nvim-lua/plenary.nvim',
        {
            'nvim-telescope/telescope-fzf-native.nvim',
            build = 'make',
        },
        {
            'nvim-telescope/telescope-live-grep-args.nvim',
        },
        "kdheepak/lazygit.nvim",
    },
    config = function()
        require('telescope').load_extension('fzf')
        require('telescope').load_extension('live_grep_args')
        require("telescope").load_extension("lazygit")
    end,
    init = function()
        vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = 'Search Files' })
        vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = 'Search current Word' })
        vim.keymap.set('n', '<leader>sg', require('telescope').extensions.live_grep_args.live_grep_args, { desc = 'Search by Grep' })
        vim.keymap.set('n', '<leader>lg', require("telescope").extensions.lazygit.lazygit, { desc = 'Open LazyGit' })
    end,
}

return plugin