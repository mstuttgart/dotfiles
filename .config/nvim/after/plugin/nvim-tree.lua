-- nvim-tree settings

local status, nvimtree = pcall(require, 'nvim-tree')

if (not status) then return end

vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

vim.opt.termguicolors = true

nvimtree.setup({
  disable_netrw = true,
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
    enable = true,
    ignore = false,
    show_on_dirs = true,
    show_on_open_dirs = true,
    timeout = 400,
  },
  renderer = {
    indent_markers = {
      enable = true,
      icons = {
        corner = "└ ",
        edge = "┆' ",
        item = "┆' ",
        none = "  ",
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
          unstaged = "", -- 
          staged = "",
          unmerged = "",
          renamed = "➜",
          untracked = "",
          deleted = "",
          ignored = "◌",
        },
      },
    },
  }

})

vim.cmd[[hi NvimTreeNormal guibg=NONE ctermbg=NONE]]
vim.cmd[[hi NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE]]

-- nvim-tree
vim.keymap.set('n', '<Leader>ee', ':NvimTreeToggle<CR>', ns)
vim.keymap.set('n', '<Leader>ef', ':NvimTreeFindFile<CR>', ns)
