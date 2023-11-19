-- coding plugins

local plugins = {
    -- snippets engine
    {

        'L3MON4D3/LuaSnip',
        event = 'VeryLazy',

    },
    -- snippets collection
    {
        'rafamadriz/friendly-snippets',
        event = 'VeryLazy',
    },

    -- highlight for color code
    {
        'norcalli/nvim-colorizer.lua',
        event = 'VeryLazy',
        config = function()
            require('colorizer').setup(nil, { css = true })
        end,
    },

    -- csv highlight
    {
        'mechatroner/rainbow_csv',
        event = 'VeryLazy',
    },

    -- word highlight
    {
        'echasnovski/mini.cursorword',
        event = 'VeryLazy',
        version = '*',
        config = function()
            require('mini.cursorword').setup()
        end,
    },

    -- auto close pairs
    {
        'echasnovski/mini.pairs',
        version = '*',
        event = 'VeryLazy',
        config = function()
            require('mini.cursorword').setup()
        end,
    },

    -- comment
    {
        'echasnovski/mini.comment',
        version = '*',
        event = 'VeryLazy',
        opts = {},
        config = function()
            require("mini.comment").setup {
                options = {
                    -- Whether to ignore blank lines
                    ignore_blank_line = true,
                },
            }
        end
    },

    -- surround
    {
        'echasnovski/mini.surround',
        version = '*',
        event = 'VeryLazy',
        config = function()
            require('mini.cursorword').setup()
        end,
    },

    -- add code docs
    {
        'danymat/neogen',
        config = true,
        event = 'VeryLazy',
        init = function()
            vim.keymap.set(
                'n',
                '<Leader>cd',
                ':lua require("neogen").generate()<CR>',
                { silent = true, desc = 'Generate Documentation' }
            )
        end,
    },

    -- better scape shortcuts
    {
        "max397574/better-escape.nvim",
        event = "InsertEnter",
        config = function()
            require("better_escape").setup()
        end,
    },

    -- install odoo snippets
    {
        "mstuttgart/vscode-odoo-snippets",
        event = "InsertEnter",
        dependencies = {
            "L3MON4D3/LuaSnip",
        },
        config = function()
            require("luasnip.loaders.from_vscode").lazy_load()
        end,
    },

    -- configure linters
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

    -- configure autoformatters
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

    -- Configure mason to autoinstall linters and formatters
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
                    -- linters
                    "eslint_d",
                    "shellcheck",
                    "pylint",

                    -- formatters
                    "autopep8",
                    "isort",
                    "prettier",
                    "shfmt",
                    "stylua",
                    "xmlformatter",
                },
            })
        end,
    },


}

return plugins
