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
            }
        end,
    },

    -- add code documentation
    {
        "danymat/neogen",
        event = "VeryLazy",
        dependencies = {
            "nvim-treesitter/nvim-treesitter",
        },
        config = function()
            require("neogen").setup {
                enabled = true,
                snippet_engine = "luasnip",
                languages = {
                    python = {
                        template = {
                            annotation_convention = "google_docstrings"
                        }
                    },
                },
            }
        end,
        init = function()
            vim.keymap.set("n", "<leader>cd", ":lua require('neogen').generate()<CR>",
                { silent = true, desc = "Generate Documentation" }
            )
        end,
    },

    -- nvim colorizer color code
    {
        "norcalli/nvim-colorizer.lua",
        event = "VeryLazy",
        config = function()
            require("colorizer").setup({ "css", "javascript", "lua", "vim", "toml", "svelte", "typescript", "conf" }, {
                RGB = true,          -- #RGB hex codes
                RRGGBB = true,       -- #RRGGBB hex codes
                names = false,       -- "Name" codes like Blue oe blue
                RRGGBBAA = true,     -- #RRGGBBAA hex codes
                rgb_fn = true,       -- CSS rgb() and rgba() functions
                hsl_fn = true,       -- CSS hsl() and hsla() functions
                css = true,          -- Enable all CSS features: rgb_fn, hsl_fn, names, RGB, RRGGBB
                css_fn = true,       -- Enable all CSS *functions*: rgb_fn, hsl_fn
                -- Available modes: foreground, background, virtualtext
                mode = "background", -- Set the display mode.)
            })
        end,
    }


}

return plugins
