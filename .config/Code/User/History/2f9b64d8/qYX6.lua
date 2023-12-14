-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    dependencies = {
        "WhoIsSethDaniel/mason-tool-installer.nvim",
    },
    event = { "BufReadPre", "BufNewFile" },
    lazy = true,
    keys = {
        {
            "<leader>cf",
            function()
                require("conform").format({ async = true, lsp_fallback = true })
            end,
            mode = "",
            desc = "Format buffer",
        },
    },
    opts = {
        -- Define formatters
        formatters_by_ft = {
            bash = { "shfmt" },
            css = { "prettier" },
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

    },
}

return plugin
