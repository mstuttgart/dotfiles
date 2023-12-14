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
                bash = { 'beautysh' },
            },
        }
    end,
    init = function()
        vim.keymap.set('n', '<leader>fm', require("conform").format, { desc = '[F]ormat File' })
    end,
}

return plugin
