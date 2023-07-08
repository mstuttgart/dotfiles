-- spectre settings

-- Fuzzy Finder (files, lsp, etc)
local plugin = {
    'nvim-pack/nvim-spectre',
    dependencies = {
        'nvim-lua/plenary.nvim',
    },
    -- config = function()
    --     require('telescope').load_extension('fzf')
    -- end,
    init = function()
        -- vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = '[S]earch [F]iles' })
        -- vim.keymap.set('n', '<leader>sh', require('telescope.builtin').help_tags, { desc = '[S]earch [H]elp' })
        -- vim.keymap.set(
        --     'n',
        --     '<leader>sw',
        --     require('telescope.builtin').grep_string,
        --     { desc = '[S]earch current [W]ord' }
        -- )
        -- vim.keymap.set('n', '<leader>sg', require('telescope.builtin').live_grep, { desc = '[S]earch by [G]rep' })
        -- vim.keymap.set('n', '<leader>sd', require('telescope.builtin').diagnostics, { desc = '[S]earch [D]iagnostics' })
        vim.keymap.set('n', '<leader>S', '<cmd>lua require("spectre").open()<CR>', {
            desc = 'Open Spectre',
        })
        vim.keymap.set('n', '<leader>sw', '<cmd>lua require("spectre").open_visual({select_word=true})<CR>', {
            desc = 'Spectre - search current word',
        })
        vim.keymap.set('v', '<leader>sw', '<esc><cmd>lua require("spectre").open_visual()<CR>', {
            desc = 'Spectre - search current word',
        })
        vim.keymap.set('n', '<leader>sp', '<cmd>lua require("spectre").open_file_search({select_word=true})<CR>', {
            desc = 'Search on current file',
        })
    end,
}

return plugin
