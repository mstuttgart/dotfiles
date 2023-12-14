local M = {}

-- git support in nvimtree
M.nvimtree = {
  filters = {
    dotfiles = false,
    custom = { "^\\.git$", "__pycache__" },
  },
  view = {
    adaptive_size = true,
    side = "left",
    width = 50,
    preserve_window_proportions = true,
  },
  renderer = {
    indent_markers = {
      enable = true,
      icons = {
        corner = "└ ",
        edge = "┆ ",
        item = "┆ ",
        none = "  ",
      },
    },
  },
}

-- override indent_blankline
M.indent_blankline = {
  char = "┆",
  show_trailing_blankline_indent = false,
  show_first_indent_level = false,
  use_treesitter = true,
  show_current_context = true,
  show_end_of_line = true,
  space_char_blankline = " ",
}

-- override gitsigs
M.gitsigns = {
  current_line_blame = true,
  current_line_blame_formatter_opts = {
    relative_time = false,
  },
}

return M
