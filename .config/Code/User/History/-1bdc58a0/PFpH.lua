vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {

    -- {
    --     "nvim-neo-tree/neo-tree.nvim",
    --     branch = "v3.x",
    --     dependencies = {
    --       "nvim-lua/plenary.nvim",
    --       "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
    --       "MunifTanjim/nui.nvim",
    --       -- "3rd/image.nvim", -- Optional image support in preview window: See `# Preview Mode` for more information
    --     },
    --     cmd = "Neotree",
    --     keys = {
    --         {
    --             "<leader>fe",
    --             function()
    --                 require("neo-tree.command").execute({ toggle = true, dir = Util.root() })
    --             end,
    --             desc = "Explorer NeoTree (root dir)",
    --         },
    --         {
    --             "<leader>fE",
    --             function()
    --                 require("neo-tree.command").execute({ toggle = true, dir = vim.loop.cwd() })
    --             end,
    --             desc = "Explorer NeoTree (cwd)",
    --         },
    --         { "<leader>e", "<leader>fe", desc = "Explorer NeoTree (root dir)", remap = true },
    --         { "<leader>E", "<leader>fE", desc = "Explorer NeoTree (cwd)",      remap = true },
    --         {
    --             "<leader>ge",
    --             function()
    --                 require("neo-tree.command").execute({ source = "git_status", toggle = true })
    --             end,
    --             desc = "Git explorer",
    --         },
    --         {
    --             "<leader>be",
    --             function()
    --                 require("neo-tree.command").execute({ source = "buffers", toggle = true })
    --             end,
    --             desc = "Buffer explorer",
    --         },
    --     },
    --     deactivate = function()
    --         vim.cmd([[Neotree close]])
    --     end,
    --     init = function()
    --         if vim.fn.argc(-1) == 1 then
    --             local stat = vim.loop.fs_stat(vim.fn.argv(0))
    --             if stat and stat.type == "directory" then
    --                 require("neo-tree")
    --             end
    --         end
    --     end,
    --     opts = {
    --         sources = { "filesystem", "buffers", "git_status", "document_symbols" },
    --         open_files_do_not_replace_types = { "terminal", "Trouble", "trouble", "qf", "Outline" },
    --         filesystem = {
    --             bind_to_cwd = false,
    --             follow_current_file = { enabled = true },
    --             use_libuv_file_watcher = true,
    --         },
    --         window = {
    --             mappings = {
    --                 ["<space>"] = "none",
    --             },
    --         },
    --         default_component_configs = {
    --             indent = {
    --                 with_expanders = true, -- if nil and file nesting is enabled, will enable expanders
    --                 expander_collapsed = "",
    --                 expander_expanded = "",
    --                 expander_highlight = "NeoTreeExpander",
    --             },
    --         },
    --     },
    --     config = function(_, opts)
    --         local function on_move(data)
    --             Util.lsp.on_rename(data.source, data.destination)
    --         end

    --         local events = require("neo-tree.events")
    --         opts.event_handlers = opts.event_handlers or {}
    --         vim.list_extend(opts.event_handlers, {
    --             { event = events.FILE_MOVED,   handler = on_move },
    --             { event = events.FILE_RENAMED, handler = on_move },
    --         })
    --         require("neo-tree").setup(opts)
    --         vim.api.nvim_create_autocmd("TermClose", {
    --             pattern = "*lazygit",
    --             callback = function()
    --                 if package.loaded["neo-tree.sources.git_status"] then
    --                     require("neo-tree.sources.git_status").refresh()
    --                 end
    --             end,
    --         })
    --     end,
    -- },

    -- A file explorer tree for neovim written in lua
    {
        'nvim-tree/nvim-tree.lua',
        -- lazy = true,
        cmd = { "NvimTreeToggle", "NvimTreeFocus" },
        dependencies = {
            'nvim-tree/nvim-web-devicons',
        },
        keys = {
            { '<leader>ee', '<cmd> NvimTreeFocus <CR>',    desc = 'Focus nvimtree' },
            { '<leader>et', '<cmd> NvimTreeToggle <CR>',   desc = 'Toogle nvimtree' },
            { '<leader>ef', '<cmd> NvimTreeFindFile <CR>', desc = 'nvimtree open with current File' },
            { '<leader>er', '<cmd> NvimTreeRefresh <CR>',  desc = 'nvimtree Refresh' },
            { "<leader>ec", "<cmd> NvimTreeCollapse<CR>",  desc = "Collapse file explorer" },
        },
        opts = {
            filters = {
                dotfiles = false,
                exclude = { vim.fn.stdpath "config" .. "/lua/custom" },
            },
            disable_netrw = true,
            hijack_netrw = true,
            hijack_cursor = true,
            hijack_unnamed_buffer_when_opening = false,
            sync_root_with_cwd = true,
            update_focused_file = {
                enable = true,
                update_root = false,
            },
            view = {
                adaptive_size = false,
                side = "left",
                width = 30,
                preserve_window_proportions = true,
            },
            git = {
                enable = false,
                ignore = true,
            },
            filesystem_watchers = {
                enable = true,
            },
            actions = {
                open_file = {
                    resize_window = true,
                },
            },
            renderer = {
                root_folder_label = false,
                highlight_git = false,
                highlight_opened_files = "none",

                indent_markers = {
                    enable = false,
                },

                icons = {
                    show = {
                        file = true,
                        folder = true,
                        folder_arrow = true,
                        git = false,
                    },

                    glyphs = {
                        default = "󰈚",
                        symlink = "",
                        folder = {
                            default = "",
                            empty = "",
                            empty_open = "",
                            open = "",
                            symlink = "",
                            symlink_open = "",
                            arrow_open = "",
                            arrow_closed = "",
                        },
                        git = {
                            unstaged = "✗",
                            staged = "✓",
                            unmerged = "",
                            renamed = "➜",
                            untracked = "★",
                            deleted = "",
                            ignored = "◌",
                        },
                    },
                },
            },
        },
        init = function()
            -- add theme to nvim-tree background1
            vim.cmd('autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE')
            vim.cmd('autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE')
        end,
        config = function(_, opts)
            require("nvim-tree").setup(opts)
        end,
        -- config = function()
        -- remove default mappings
        -- local function my_on_attach(bufnr)
        --     local api = require "nvim-tree.api"

        --     local function opts(desc)
        --         return { desc = "nvim-tree: " .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
        --     end

        --     -- default mappings
        --     api.config.mappings.default_on_attach(bufnr)

        --     -- custom mappings
        --     vim.keymap.set('n', '<C-v>', api.node.open.vertical, opts('Open: Vertical Split'))
        --     vim.keymap.set('n', '<C-h>', api.node.open.horizontal, opts('Open: Horizontal Split'))
        --     vim.keymap.set('n', '<CR>', api.node.open.edit, opts('Open'))
        --     vim.keymap.set('n', '<Tab>', api.node.open.preview, opts('Open Preview'))
        --     vim.keymap.set('n', '>', api.node.navigate.sibling.next, opts('Next Sibling'))
        --     vim.keymap.set('n', '<', api.node.navigate.sibling.prev, opts('Previous Sibling'))
        --     vim.keymap.set('n', '.', api.node.run.cmd, opts('Run Command'))
        --     vim.keymap.set('n', 'a', api.fs.create, opts('Create'))
        --     vim.keymap.set('n', 'B', api.tree.toggle_no_buffer_filter, opts('Toggle Filter: No Buffer'))
        --     vim.keymap.set('n', 'c', api.fs.copy.node, opts('Copy'))
        --     vim.keymap.set('n', '[c', api.node.navigate.git.prev, opts('Prev Git'))
        --     vim.keymap.set('n', ']c', api.node.navigate.git.next, opts('Next Git'))
        --     vim.keymap.set('n', 'd', api.fs.remove, opts('Delete'))
        --     vim.keymap.set('n', 'D', api.fs.trash, opts('Trash'))
        --     vim.keymap.set('n', 'E', api.tree.expand_all, opts('Expand All'))
        --     vim.keymap.set('n', ']e', api.node.navigate.diagnostics.next, opts('Next Diagnostic'))
        --     vim.keymap.set('n', '[e', api.node.navigate.diagnostics.prev, opts('Prev Diagnostic'))
        --     vim.keymap.set('n', 'g?', api.tree.toggle_help, opts('Help'))
        --     vim.keymap.set('n', 'gy', api.fs.copy.absolute_path, opts('Copy Absolute Path'))
        --     vim.keymap.set('n', 'H', api.tree.toggle_hidden_filter, opts('Toggle Filter: Dotfiles'))
        --     vim.keymap.set('n', 'I', api.tree.toggle_gitignore_filter, opts('Toggle Filter: Git Ignore'))
        --     vim.keymap.set('n', 'J', api.node.navigate.sibling.last, opts('Last Sibling'))
        --     vim.keymap.set('n', 'K', api.node.navigate.sibling.first, opts('First Sibling'))
        --     vim.keymap.set('n', 'o', api.node.open.edit, opts('Open'))
        --     vim.keymap.set('n', 'O', api.node.open.no_window_picker, opts('Open: No Window Picker'))
        --     vim.keymap.set('n', 'p', api.fs.paste, opts('Paste'))
        --     vim.keymap.set('n', 'P', api.node.navigate.parent, opts('Parent Directory'))
        --     vim.keymap.set('n', 'q', api.tree.close, opts('Close'))
        --     vim.keymap.set('n', 'r', api.fs.rename, opts('Rename'))
        --     vim.keymap.set('n', 'R', api.tree.reload, opts('Refresh'))
        --     vim.keymap.set('n', 's', api.node.run.system, opts('Run System'))
        --     vim.keymap.set('n', 'S', api.tree.search_node, opts('Search'))
        --     vim.keymap.set('n', 'u', api.fs.rename_full, opts('Rename: Full Path'))
        --     vim.keymap.set('n', 'U', api.tree.toggle_custom_filter, opts('Toggle Filter: Hidden'))
        --     vim.keymap.set('n', 'C', api.tree.collapse_all, opts('Collapse'))
        --     vim.keymap.set('n', 'x', api.fs.cut, opts('Cut'))
        --     vim.keymap.set('n', 'y', api.fs.copy.filename, opts('Copy Name'))
        --     vim.keymap.set('n', 'Y', api.fs.copy.relative_path, opts('Copy Relative Path'))
        --     vim.keymap.set('n', '<2-LeftMouse>', api.node.open.edit, opts('Open'))
        --     vim.keymap.set('n', '<2-RightMouse>', api.tree.change_root_to_node, opts('CD'))
        -- end

        -- require("nvim-tree").setup {
        --     on_attach = my_on_attach,
        -- }
        -- end
    },

    -- Find the enemy and replace them with dark power.
    {
        "nvim-pack/nvim-spectre",
        build = false,
        cmd = "Spectre",
        opts = { open_cmd = "noswapfile vnew" },
        -- stylua: ignore
        keys = {
            { "<leader>sr", function() require("spectre").open() end, desc = "Replace in files (Spectre)" },
        },
    },

    -- Find, Filter, Preview, Pick. All lua, all the time.
    {
        'nvim-telescope/telescope.nvim',
        branch = '0.1.x',
        dependencies = {
            'nvim-lua/plenary.nvim',
            'nvim-tree/nvim-tree.lua',
            {
                'nvim-telescope/telescope-fzf-native.nvim',
                build = 'make',
            },
        },
        keys = {
            -- git
            { "<leader>gc", "<cmd>Telescope git_commits<CR>", desc = "commits" },
            { "<leader>gs", "<cmd>Telescope git_status<CR>",  desc = "status" },
        },
        config = function()
            require('telescope').load_extension('fzf')
        end,
        init = function()
            vim.keymap.set('n', '<leader>sf', require('telescope.builtin').find_files, { desc = 'Search Files' })
            vim.keymap.set('n', '<leader>sw', require('telescope.builtin').grep_string, { desc = 'Search current Word' })
        end,
    },

    -- Git integration for buffers
    {
        "lewis6991/gitsigns.nvim",
        opts = {
            current_line_blame = false,
            current_line_blame_formatter_opts = {
                relative_time = false,
            },
            signs = {
                add = { text = "▎" },
                change = { text = "▎" },
                delete = { text = "➤" },
                topdelete = { text = "➤" },
                changedelete = { text = "▎" },
            },
            on_attach = function(bufnr)
                local gs = package.loaded.gitsigns

                local function map(mode, l, r, desc)
                    vim.keymap.set(mode, l, r, { buffer = bufnr, desc = desc })
                end

                map("n", "<leader>gb", function() gs.blame_line({ full = true }) end, "Blame Line")
                map("n", "<leader>gt", gs.toggle_current_line_blame, "Toogle Blame Line")
                map("n", "<leader>gd", gs.diffthis, "Diff This")
                map("n", "<leader>gD", function() gs.diffthis("~") end, "Diff This ~")
            end,
        },
    },

    -- see code tags
    {
        'simrat39/symbols-outline.nvim',
        cmd = 'SymbolsOutline',
        keys = {
            { '<leader>ct', '<cmd>SymbolsOutline<cr>', desc = 'Code Tags (Symbols Outline)' },
        },
        config = function()
            require('symbols-outline').setup({
                vim.api.nvim_create_autocmd(
                    'BufEnter',
                    {
                        pattern = '*',
                        command = 'hi SymbolsOutlineConnector gui=none guifg=vim.g.foreground',
                    }
                )
            })
        end
    },

    -- terminal emulator
    {
        "NvChad/nvterm",
        config = function()
            require("nvterm").setup()
        end,
        init = function()
            vim.keymap.set({ 'n', 't' }, '<leader>;', function() require("nvterm.terminal").toggle('horizontal') end,
                { silent = true })
        end
    }

}

return plugins
