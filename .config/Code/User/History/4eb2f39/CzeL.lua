-- nvim-tree settings

vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugin = {
    'nvim-tree/nvim-tree.lua', -- no more netrw
    opts = {
        sync_root_with_cwd = true,
        respect_buf_cwd = true,
        update_focused_file = {
            enable = true,
            update_root = true,
        },
        filters = {
            dotfiles = false,
        },
        view = {
            adaptive_size = true,
            side = 'left',
            preserve_window_proportions = false,
        },
        git = {
            enable = true, -- show git statuses
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
    },
    keys = {
        { '<leader>ee', '<cmd>NvimTreeToggle<cr>', desc = 'Toggle  Tree' },
        { '<leader>ef', '<cmd>NvimTreeFindFile<cr>', desc = 'Tree open with current File' },
        { '<leader>er', '<cmd>NvimTreeRefresh<cr>', desc = 'Tree Refresh' },
    },
    init = function()
        vim.cmd('autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE')
        vim.cmd('autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE')
    end,
}

return plugin
