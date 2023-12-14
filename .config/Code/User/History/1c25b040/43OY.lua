local plugin = {
    {
        "mfussenegger/nvim-lint",
        event = {
            "BufReadPre",
            "BufNewFile",
        },
        config = function()
            local lint = require("lint")

            lint.linters_by_ft = {
                ansible = { "ansible_lint" },
                bash = { "shellcheck" },
                javascript = { "eslint_d" },
                python = { "pylint" },
                typescript = { "eslint_d" },
            }

            vim.api.nvim_create_autocmd({ "BufWritePost" }, {
                callback = function()
                    lint.try_lint()
                end,
            })
        end,
    },

    -- Configure mason to autoinstall linters
    {
        "williamboman/mason.nvim",
        dependencies = {
            "WhoIsSethDaniel/mason-tool-installer.nvim",
        },
        config = function()
            local mason = require("mason")

            -- mason formatter linters
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
                    "ansible_lint",
                    "eslint_d",
                    "shellcheck",
                    "pylint",
                },
            })
        end,
    },
}

return plugin
