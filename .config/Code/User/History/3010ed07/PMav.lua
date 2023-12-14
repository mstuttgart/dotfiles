-- formatting , linting
local plugin = {
    "stevearc/conform.nvim",
    lazy = true,
    config = function()
        require("conform").setup {
            formatters_by_ft = {
                lua = { "stylua" },
                javascript = { { "prettier" } },
                python = { 'autopep8' },
            },
        }
    end,
    init = function()
        vim.keymap.set('n', '<leader>fm', require("conform").format(), { desc = '[S]earch [F]iles' })
        vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = '[S]earch current [W]ord' })
        vim.keymap.set('n', '<leader>sg', require('telescope').extensions.live_grep_args.live_grep_args, { desc = '[S]earch by [G]rep' })
    end,
}

return plugin
