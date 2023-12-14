---@type NvPluginSpec[]
local plugins = {

    -- configure syntax highlight
    {
        "nvim-treesitter/nvim-treesitter",
        opts = {
            -- Add languages to be installed here that you want installed for treesitter
            ensure_installed = {
                "bash",
                "css",
                "html",
                "javascript",
                "json",
                "lua",
                "markdown_inline",
                "markdown",
                "python",
                "query",
                "regex",
                "toml",
                "xml",
                "yaml",
            },
            -- Autoinstall languages that are not installed. Defaults to false (but you can change for yourself!)
            auto_install = true,
            highlight = {
                enable = true,
            },
            indent = {
                enable = true,
                disable = { "python" },
            },
            context_commentstring = {
                enable = false,
                enable_autocmd = false,
                config = {
                    python = "# %s",
                },
            },
        },
    },

    -- In order to modify the `lspconfig` configuration:
    {
        "neovim/nvim-lspconfig",
        config = function()
            require "plugins.configs.lspconfig"
            require "custom.configs.lspconfig"
        end,
    },

    -- configure mason
    {
        "williamboman/mason.nvim",
        opts = {
            ensure_installed = {
                -- lsp
                "ansible-language-server",
                "bash-language-server",
                "css-lsp",
                "html-lsp",
                "lua-language-server",
                "pyright",
                "typescript-language-server",

                -- lint
                -- linters
                "eslint_d",
                "pylint",
                "shellcheck",

                -- formatters
                "autopep8",
                "isort",
                "prettier",
                "shfmt",
                "stylua",
                "xmlformatter",
                "yamlfmt",
            },
            -- auto-install configured servers (with lspconfig)
            automatic_installation = true,
        },
    }




}

return plugins
