-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    event = { "BufReadPre", "BufNewFile" },
    config = function()
        require("conform").setup({
            formatters_by_ft = {
                css = { "prettier" },
                graphql = { "prettier" },
                html = { "prettier" },
                javascript = { "prettier" },
                json = { "prettier" },
                lua = { "stylua" },
                markdown = { "prettier" },
                python = { "isort", "autopep8" },
                typescript = { "prettier" },
                xml = { "xmlformat" },
                yaml = { "prettier" },
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
