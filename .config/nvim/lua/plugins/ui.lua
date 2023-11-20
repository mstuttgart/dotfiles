-- ui plugins settings

local plugins = {

    -- amazing web icons
    { "nvim-tree/nvim-web-devicons", lazy = true },

    -- smooth scroll
    {
        "karb94/neoscroll.nvim",
        config = function()
            require("neoscroll").setup {}
        end
    },

    -- plugin to visualize and operate on indent scope.
    {
        "echasnovski/mini.indentscope",
        version = false, -- wait till new 0.7.0 release to put it back on semver
        event = {
            "BufReadPre",
            "BufNewFile",
        },
        opts = {
            symbol = "┆",
            options = { try_as_border = true },
        },
        init = function()
            vim.api.nvim_create_autocmd("FileType", {
                pattern = {
                    "alpha",
                    "dashboard",
                    "help",
                    "lazy",
                    "lazyterm",
                    "mason",
                    "neo-tree",
                    "notify",
                    "toggleterm",
                    "trouble",
                    "Trouble",
                },
                callback = function()
                    vim.b.miniindentscope_disable = true
                end,
            })
        end,
    },

    -- Useful plugin to show you pending keybinds.
    {
        "folke/which-key.nvim",
        event = "VeryLazy",
        init = function()
            vim.o.timeout = true
            vim.o.timeoutlen = 300
        end,
        opts = {
            plugins = { spelling = true },
            defaults = {
                mode = { "n", "v" },
                ["g"] = { name = "+goto" },
                ["gs"] = { name = "+surround" },
                ["]"] = { name = "+next" },
                ["["] = { name = "+prev" },
                ["<leader><tab>"] = { name = "+tabs" },
                ["<leader>b"] = { name = "+buffer" },
                ["<leader>c"] = { name = "+code" },
                ["<leader>f"] = { name = "+file/find" },
                ["<leader>g"] = { name = "+git" },
                ["<leader>gh"] = { name = "+hunks" },
                ["<leader>q"] = { name = "+quit/session" },
                ["<leader>s"] = { name = "+search" },
                ["<leader>u"] = { name = "+ui" },
                ["<leader>w"] = { name = "+windows" },
                ["<leader>x"] = { name = "+diagnostics/quickfix" },
            },
        },
        config = function(_, opts)
            local wk = require("which-key")
            wk.setup(opts)
            wk.register(opts.defaults)
        end,
    },

    -- A snazzy bufferline for Neovim
    {
        "akinsho/bufferline.nvim",
        dependencies = {
            { "echasnovski/mini.bufremove", version = "*" },
        },
        event = "VeryLazy",
        keys = {
            { "<leader>bQ", "<Cmd>BufferLineGroupClose ungrouped<CR>", desc = "Delete non-pinned buffers" },
            { "<leader>bo", "<Cmd>BufferLineCloseOthers<CR>",          desc = "Delete other buffers" },
            { "<leader>br", "<Cmd>BufferLineCloseRight<CR>",           desc = "Delete buffers to the right" },
            { "<leader>bl", "<Cmd>BufferLineCloseLeft<CR>",            desc = "Delete buffers to the left" },
            { "<Tab>",      "<cmd>BufferLineCyclePrev<cr>",            desc = "Prev buffer" },
            { "<S-Tab>",    "<cmd>BufferLineCycleNext<cr>",            desc = "Next buffer" },
        },
        opts = {
            options = {
                close_command = function(n)
                    require("mini.bufremove").delete(n, false)
                end,
                right_mouse_command = function(n)
                    require("mini.bufremove").delete(n, false)
                end,
                diagnostics = "nvim_lsp",
                separator_style = "thin",
                always_show_bufferline = true,
                offsets = {
                    {
                        filetype = "NvimTree",
                        text = "",
                        highlight = "Directory",
                        text_align = "left",
                        separator = false,
                    },
                },
            },
        },
    },

    -- A blazing fast and easy to configure neovim statusline plugin
    {
        'nvim-lualine/lualine.nvim',
        -- dependencies = {
        --     'arkav/lualine-lsp-progress',
        -- },
        event = 'VeryLazy',
        opts = function()
            return {
                options = {
                    theme = 'auto',
                    globalstatus = true,
                    disabled_filetypes = { statusline = { 'dashboard', 'alpha' } },
                },
                sections = {
                    lualine_a = { 'mode' },
                    lualine_b = { 'branch' },
                    lualine_c = {
                        {
                            'diagnostics',
                            error = ' ',
                            warn = ' ',
                            info = ' ',
                            hint = ' ',
                        },
                        {
                            'filetype',
                            icon_only = true,
                            separator = '',
                            padding = {
                                left = 1,
                                right = 0,
                            },
                        },
                        -- {
                        --     'lsp_progress',
                        -- },
                        {
                            'filename',
                            path = 1,
                            symbols = { modified = '  ', readonly = '', unnamed = '' },
                        },
                    },
                    lualine_x = {
                        -- stylua: ignore
                        {
                            function() return require("noice").api.status.command.get() end,
                            cond = function()
                                return package.loaded["noice"] and
                                    require("noice").api.status.command.has()
                            end,
                        },
                        -- stylua: ignore
                        {
                            function() return require("noice").api.status.mode.get() end,
                            cond = function() return package.loaded["noice"] and require("noice").api.status.mode.has() end,
                        },
                        {
                            "diff",
                            symbols = {
                                added = " ",
                                modified = " ",
                                removed = " ",
                            },
                            source = function()
                                local gitsigns = vim.b.gitsigns_status_dict
                                if gitsigns then
                                    return {
                                        added = gitsigns.added,
                                        modified = gitsigns.changed,
                                        removed = gitsigns.removed,
                                    }
                                end
                            end,
                        },
                    },
                    lualine_y = {
                        { 'progress', separator = ' ',                  padding = { left = 1, right = 0 } },
                        { 'location', padding = { left = 0, right = 1 } },
                    },
                    lualine_z = {
                        function()
                            return ' ' .. os.date('%R')
                        end,
                    },
                },
                extensions = { 'nvim-tree', 'lazy' },
            }
        end,
    },

    -- navic complement to breadcumbs
    {
        'utilyre/barbecue.nvim',
        version = '*',
        dependencies = {
            'SmiteshP/nvim-navic',
            'nvim-tree/nvim-web-devicons',
        },
        config = true,
    },

    -- better vim.ui
    {
        "stevearc/dressing.nvim",
        lazy = true,
        init = function()
            ---@diagnostic disable-next-line: duplicate-set-field
            vim.ui.select = function(...)
                require("lazy").load({ plugins = { "dressing.nvim" } })
                return vim.ui.select(...)
            end
            ---@diagnostic disable-next-line: duplicate-set-field
            vim.ui.input = function(...)
                require("lazy").load({ plugins = { "dressing.nvim" } })
                return vim.ui.input(...)
            end
        end,
    },

    -- override nvim ui
    {
        'folke/noice.nvim',
        event = 'VeryLazy',
        dependencies = {
            'nvim-treesitter/nvim-treesitter',
            'MunifTanjim/nui.nvim',
        },
        opts = {
            lsp = {
                override = {
                    ["vim.lsp.util.convert_input_to_markdown_lines"] = true,
                    ["vim.lsp.util.stylize_markdown"] = true,
                    ["cmp.entry.get_documentation"] = true,
                },
            },
            routes = {
                {
                    filter = {
                        event = "msg_show",
                        any = {
                            { find = "%d+L, %d+B" },
                            { find = "; after #%d+" },
                            { find = "; before #%d+" },
                        },
                    },
                    view = "mini",
                },
            },
            presets = {
                bottom_search = true,
                command_palette = true,
                long_message_to_split = true,
                inc_rename = true,
            },
        },
    },

    -- notify ui
    {
        "rcarriga/nvim-notify",
        keys = {
            {
                "<leader>un",
                function()
                    require("notify").dismiss({ silent = true, pending = true })
                end,
                desc = "Dismiss all Notifications",
            },
        },
        opts = {
            timeout = 2000,
            max_height = function()
                return math.floor(vim.o.lines * 0.75)
            end,
            max_width = function()
                return math.floor(vim.o.columns * 0.75)
            end,
            on_open = function(win)
                vim.api.nvim_win_set_config(win, { zindex = 100 })
            end,
        },
    },

}

return plugins