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

    {
        "nvim-tree/nvim-tree.lua",
        opts = overrides.nvimtree,
      },
    
      {
        "lukas-reineke/indent-blankline.nvim",
        opts = overrides.indent_blankline,
      },
    
      {
        "lewis6991/gitsigns.nvim",
        opts = overrides.gitsigns,
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

    -- csv highlight
    {
        "mechatroner/rainbow_csv",
        event = "VeryLazy",
    },

    -- word highlight
    {
        "echasnovski/mini.cursorword",
        event = "VeryLazy",
        version = "*",
        config = function()
            require("mini.cursorword").setup()
        end,
    },

    -- surround
    {
        "kylechui/nvim-surround",
        version = "*",
        event = "VeryLazy",
        dependencies = {
            "nvim-treesitter/nvim-treesitter",
            "nvim-treesitter/nvim-treesitter-textobjects",
        },
        config = function()
            require("nvim-surround").setup()
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

    -- smooth scroll
    {
        "karb94/neoscroll.nvim",
        config = function()
            require("neoscroll").setup {}
        end,
    },

    -- navic complement to breadcumbs
    {
        "utilyre/barbecue.nvim",
        version = "*",
        dependencies = {
            "SmiteshP/nvim-navic",
            "nvim-tree/nvim-web-devicons",
        },
        config = true,
    },


}

return plugins
