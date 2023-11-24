-- A file explorer tree for neovim written in lua

vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {
    "nvim-tree/nvim-tree.lua",
    cmd = { "NvimTreeToggle", "NvimTreeFocus" },
    dependencies = {
        "nvim-tree/nvim-web-devicons",
    },
    keys = {
        { "<leader>ee", "<cmd> NvimTreeFocus <CR>",    desc = "Focus nvimtree" },
        { "<leader>et", "<cmd> NvimTreeToggle <CR>",   desc = "Toogle nvimtree" },
        { "<leader>ef", "<cmd> NvimTreeFindFile <CR>", desc = "nvimtree open with current File" },
        { "<leader>er", "<cmd> NvimTreeRefresh <CR>",  desc = "nvimtree Refresh" },
        { "<leader>ec", "<cmd> NvimTreeCollapse<CR>",  desc = "Collapse file explorer" },
    },
    opts = {
        filters = {
            dotfiles = false,
            custom = { "^\\.git", "__pycache__" },
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
            adaptive_size = true,
            side = "left",
            width = 30,
            preserve_window_proportions = true,
        },
        git = {
            enable = true,  -- show git statuses
            ignore = false, -- still show .gitignored files
            show_on_dirs = true,
            show_on_open_dirs = true,
            timeout = 400,
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
                enable = true,
                icons = {
                    corner = "└ ",
                    edge = "┆ ",
                    item = "┆ ",
                    none = "  ",
                },
            },
            icons = {
                webdev_colors = false,
                show = {
                    file = true,
                    folder = true,
                    folder_arrow = false,
                    git = false,
                },
                glyphs = {
                    default = "",
                    symlink = "",
                    folder = {
                        arrow_closed = "",
                        arrow_open = "",
                        default = "",
                        open = "",
                        empty = "",
                        empty_open = "",
                        symlink = "",
                        symlink_open = "",
                    },
                    git = {
                        unstaged = "",
                        staged = "",
                        unmerged = "",
                        renamed = "➜",
                        untracked = "",
                        deleted = "",
                        ignored = "◌",
                    },
                },
            },
        },
    },
    init = function()
        -- add theme to nvim-tree background1
        vim.cmd "autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE"
        vim.cmd "autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE"
    end,
    config = function(_, opts)
        require("nvim-tree").setup(opts)
    end,
}

return plugins
