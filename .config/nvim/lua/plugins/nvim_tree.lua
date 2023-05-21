-- nvim-tree settings

vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugin = {
  'nvim-tree/nvim-tree.lua', -- no more netrw
  opts = {
    -- hijack_cursor = true,
    update_focused_file = {
      enable = true,
    },
    filters = {
      dotfiles = false,
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
          git = true
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
    }
  },
  keys = {
    { '<leader>tt', '<cmd>NvimTreeToggle<cr>',   desc = '[T]oggle  [T]ree' },
    { '<leader>tf', '<cmd>NvimTreeFindFile<cr>', desc = '[T]ree open with current [F]ile' },
    { '<leader>tr', '<cmd>NvimTreeRefresh<cr>',  desc = '[T]ree [R]efresh' },
  },
  init = function()
    -- change background color of tree
    vim.cmd('autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE')
    vim.cmd('autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE')
  end
}

return plugin
