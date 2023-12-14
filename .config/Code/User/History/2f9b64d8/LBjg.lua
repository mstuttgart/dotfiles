-- configure formmating

local plugins = {
    {
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
    },
    {
        "williamboman/mason.nvim",
        dependencies = {
            "WhoIsSethDaniel/mason-tool-installer.nvim",
        },
        config = function()
            local mason = require("mason")

            -- mason formatter installer
            local mason_tool_installer = require("mason-tool-installer")

            -- enable mason and configure icons
            mason.setup({
                ui = {
                    icons = {
                        package_installed = "✓",
                        package_pending = "➜",
                        package_uninstalled = "✗",
                    },
                },
            })

            mason_tool_installer.setup({
                ensure_installed = {
                    "autopep8",
                    "eslint_d",
                    "isort",
                    "prettier",
                    "shfmt",
                    "stylua",
                    "xmlformat",
                },
            })
        end,
    }
}

return plugins
