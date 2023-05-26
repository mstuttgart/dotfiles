-- telescope settings

-- Fuzzy Finder (files, lsp, etc)
local plugin = {
    'nvim-telescope/telescope.nvim',
    branch = '0.1.x',
    dependencies = {
        { 'nvim-lua/plenary.nvim' },
        { 'nvim-telescope/telescope-fzf-native.nvim', build = 'make' },
        { 'tiagovla/scope.nvim' },
    },
    config = function()
        require('telescope').load_extension('fzf')
        require('telescope').load_extension('scope')
    end,
    init = function()
        vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = '[S]earch [F]iles' })
        vim.keymap.set('n', '<leader>sh', require('telescope.builtin').help_tags, { desc = '[S]earch [H]elp' })
        vim.keymap.set(
            'n',
            '<leader>sw',
            require('telescope.builtin').grep_string,
            { desc = '[S]earch current [W]ord' }
        )
        vim.keymap.set('n', '<leader>sg', require('telescope.builtin').live_grep, { desc = '[S]earch by [G]rep' })
        vim.keymap.set('n', '<leader>sd', require('telescope.builtin').diagnostics, { desc = '[S]earch [D]iagnostics' })
        vim.api.nvim_set_keymap('n', '<leader>sb', ':Telescope scope buffers <cr>', { desc = '[S]earch [D]iagnostics' })
    end,
}

return plugin
