-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    dependencies = { "mason.nvim" },
    lazy = true,
    cmd = "ConformInfo",
    keys = {
        {
            "<leader>cf",
            function()
                require("conform").format({
                    formatters = { "injected" },
                })
            end,
            mode = { "n", "v" },
            desc = "Format Injected Langs",
        },
    },
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
            format = {
                timeout_ms = 3000,
                async = false, -- not recommended to change
                quiet = false, -- not recommended to change
              },
        })

    end,
}

return plugin
