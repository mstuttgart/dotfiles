-- nvim-tree settings
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

vim.opt.termguicolors = true

require('nvim-tree').setup({
  disable_netrw = true,
  update_focused_file = {
      enable = true,
    },
  view = {
    adaptive_size = true,
    side = 'left',
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
