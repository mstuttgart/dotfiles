local plugins = {
    -- A file explorer tree for neovim written in lua
    {
        'nvim-tree/nvim-tree.lua',
        lazy = true,
        dependencies = {
            'nvim-tree/nvim-web-devicons',
        },
        keys = {
            { '<leader>ee', '<cmd>NvimTreeToggle<cr>',   desc = 'Toggle  Tree' },
            { '<leader>ef', '<cmd>NvimTreeFindFile<cr>', desc = 'Tree open with current File' },
            { '<leader>er', '<cmd>NvimTreeRefresh<cr>',  desc = 'Tree Refresh' },
        },
        opts = {
            disable_netrw = true,
            hijack_netrw = true,
            hijack_cursor = true,
            hijack_unnamed_buffer_when_opening = false,
            sync_root_with_cwd = true,
            update_focused_file = {
                enable = true,
                update_root = true,
            },
            filters = {
                dotfiles = false,
                custom = { "^.git$", "^__pycache__$" },
            },
            view = {
                adaptive_size = true,
                side = 'left',
            },
            git = {
                enable = true,  -- show git statuses
                ignore = false, -- still show .gitignored files
                show_on_dirs = true,
                show_on_open_dirs = true,
                timeout = 400,
            },
            renderer = {
                indent_markers = {
                    enable = true,
                    icons = {
                        corner = '└ ',
                        edge = '┆ ',
                        item = '┆ ',
                        none = '  ',
                    },
                },
                icons = {
                    webdev_colors = false,
                    show = {
                        file = true,
                        folder = true,
                        folder_arrow = false,
                        git = true,
                    },
                    glyphs = {
                        default = '',
                        symlink = '',
                        folder = {
                            arrow_closed = '',
                            arrow_open = '',
                            default = '',
                            open = '',
                            empty = '',
                            empty_open = '',
                            symlink = '',
                            symlink_open = '',
                        },
                        git = {
                            unstaged = '',
                            staged = '',
                            unmerged = '',
                            renamed = '➜',
                            untracked = '',
                            deleted = '',
                            ignored = '◌',
                        },
                    },
                },
            },
            diagnostics = {
                enable = true,
                show_on_dirs = false,
                icons = {
                    hint = "",
                    info = "",
                    warning = "",
                    error = "",
                },
            },
        },
        init = function()
            -- add theme to nvim-tree background1
            vim.cmd('autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE')
            vim.cmd('autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE')
        end,
        config = function()
            -- remove default mappings
            local function my_on_attach(bufnr)
                local api = require "nvim-tree.api"

                local function opts(desc)
                    return { desc = "nvim-tree: " .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
                end

                -- default mappings
                api.config.mappings.default_on_attach(bufnr)

                -- custom mappings
                vim.keymap.set('n', '<C-v>', api.node.open.vertical, opts('Open: Vertical Split'))
                vim.keymap.set('n', '<C-h>', api.node.open.horizontal, opts('Open: Horizontal Split'))
                vim.keymap.set('n', '<CR>', api.node.open.edit, opts('Open'))
                vim.keymap.set('n', '<Tab>', api.node.open.preview, opts('Open Preview'))
                vim.keymap.set('n', '>', api.node.navigate.sibling.next, opts('Next Sibling'))
                vim.keymap.set('n', '<', api.node.navigate.sibling.prev, opts('Previous Sibling'))
                vim.keymap.set('n', '.', api.node.run.cmd, opts('Run Command'))
                vim.keymap.set('n', 'a', api.fs.create, opts('Create'))
                vim.keymap.set('n', 'B', api.tree.toggle_no_buffer_filter, opts('Toggle Filter: No Buffer'))
                vim.keymap.set('n', 'c', api.fs.copy.node, opts('Copy'))
                vim.keymap.set('n', '[c', api.node.navigate.git.prev, opts('Prev Git'))
                vim.keymap.set('n', ']c', api.node.navigate.git.next, opts('Next Git'))
                vim.keymap.set('n', 'd', api.fs.remove, opts('Delete'))
                vim.keymap.set('n', 'D', api.fs.trash, opts('Trash'))
                vim.keymap.set('n', 'E', api.tree.expand_all, opts('Expand All'))
                vim.keymap.set('n', ']e', api.node.navigate.diagnostics.next, opts('Next Diagnostic'))
                vim.keymap.set('n', '[e', api.node.navigate.diagnostics.prev, opts('Prev Diagnostic'))
                vim.keymap.set('n', 'g?', api.tree.toggle_help, opts('Help'))
                vim.keymap.set('n', 'gy', api.fs.copy.absolute_path, opts('Copy Absolute Path'))
                vim.keymap.set('n', 'H', api.tree.toggle_hidden_filter, opts('Toggle Filter: Dotfiles'))
                vim.keymap.set('n', 'I', api.tree.toggle_gitignore_filter, opts('Toggle Filter: Git Ignore'))
                vim.keymap.set('n', 'J', api.node.navigate.sibling.last, opts('Last Sibling'))
                vim.keymap.set('n', 'K', api.node.navigate.sibling.first, opts('First Sibling'))
                vim.keymap.set('n', 'o', api.node.open.edit, opts('Open'))
                vim.keymap.set('n', 'O', api.node.open.no_window_picker, opts('Open: No Window Picker'))
                vim.keymap.set('n', 'p', api.fs.paste, opts('Paste'))
                vim.keymap.set('n', 'P', api.node.navigate.parent, opts('Parent Directory'))
                vim.keymap.set('n', 'q', api.tree.close, opts('Close'))
                vim.keymap.set('n', 'r', api.fs.rename, opts('Rename'))
                vim.keymap.set('n', 'R', api.tree.reload, opts('Refresh'))
                vim.keymap.set('n', 's', api.node.run.system, opts('Run System'))
                vim.keymap.set('n', 'S', api.tree.search_node, opts('Search'))
                vim.keymap.set('n', 'u', api.fs.rename_full, opts('Rename: Full Path'))
                vim.keymap.set('n', 'U', api.tree.toggle_custom_filter, opts('Toggle Filter: Hidden'))
                vim.keymap.set('n', 'C', api.tree.collapse_all, opts('Collapse'))
                vim.keymap.set('n', 'x', api.fs.cut, opts('Cut'))
                vim.keymap.set('n', 'y', api.fs.copy.filename, opts('Copy Name'))
                vim.keymap.set('n', 'Y', api.fs.copy.relative_path, opts('Copy Relative Path'))
                vim.keymap.set('n', '<2-LeftMouse>', api.node.open.edit, opts('Open'))
                vim.keymap.set('n', '<2-RightMouse>', api.tree.change_root_to_node, opts('CD'))
            end

            require("nvim-tree").setup {
                on_attach = my_on_attach,
            }
        end
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
