-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
        require("conform").setup({
            formatters_by_ft = {
                javascript = { "prettier" },
                typescript = { "prettier" },
                css = { "prettier" },
                html = { "prettier" },
                json = { "prettier" },
                yaml = { "prettier" },
                markdown = { "prettier" },
                graphql = { "prettier" },
                lua = { "stylua" },
                python = { "isort", "autopep8" },
                xml = { "xmlformat" },
            },
        })

        vim.keymap.set(
            { "n", "v" },
            "<leader>fm",
            function()
                require('conform').format({
                    lsp_fallback = true,
                    async = false,
                    timeout_ms = 500,
                })
            end,
            { desc = "Format file or range (in visual mode)" })
    end,
}

return plugin
