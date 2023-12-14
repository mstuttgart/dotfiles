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
        dependencies = {
            "jose-elias-alvarez/null-ls.nvim",
            config = function()
                require "custom.configs.null-ls"
            end,
        },
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
    },

    -- nvim autosession save and load
    {
        'rmagatti/auto-session',
        config = function()
            vim.o.sessionoptions = 'blank,buffers,curdir,folds,help,tabpages,winsize,winpos,terminal,localoptions'

            require('auto-session').setup {
                log_level = 'error',
                auto_session_suppress_dirs = { '~/', '~/.config', '~/Downloads', '/' },
                cwd_change_handling = {
                    post_cwd_changed_hook = function() -- example refreshing the lualine status line _after_ the cwd changes
                        require('lualine').refresh() -- refresh lualine so the new session name is displayed in the status bar
                    end,
                },
            }
        end,
    },

-- add code docu

}

return plugins
