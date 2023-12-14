-- formatting , linting
local plugin = {
    "stevearc/conform.nvim",
    lazy = true,
    config = function()
        require("conform").setup {
            formatters_by_ft = {
                lua = { "stylua" },
                javascript = { { "prettier" } }
                python = { ''},
            },
        }
    end,
}


return plugin
