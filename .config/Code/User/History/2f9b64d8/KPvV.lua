-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    dependencies = { "mason.nvim" },
    event = { "BufReadPre", "BufNewFile" },
    lazy = true,
    config = function()
        local conform = require("conform")
    end,
    keys = {
        {
            -- Customize or remove this keymap to your liking
            "<leader>cf",
            function()
                require("conform").format({ async = true, lsp_fallback = true })
            end,
            mode = "",
            desc = "Format buffer",
        },
    },
    opts = {
        -- Define your formatters
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
        -- Set up format-on-save
        -- format_on_save = { timeout_ms = 500, lsp_fallback = true },
        -- Customize formatters
        formatters = {
            shfmt = {
                prepend_args = { "-i", "2" },
            },
        },
    },
}

return plugin
