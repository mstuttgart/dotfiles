local M = {}

M.treesitter = {
  ensure_installed = {
    "vim",
    "lua",
    "html",
    "css",
    "javascript",
    "typescript",
    "c",
    "markdown",
    "markdown_inline",
    "python",
    "bash",
    "yaml",
  },
  auto_install = true,
  highlight = { enable = true },
  indent = {
    enable = true,
    disable = {
      "python",
    },
  },
}

M.mason = {
  ensure_installed = {
    -- lua stuff
    "lua-language-server",
    "stylua",

    -- web dev stuff
    "css-lsp",
    "html-lsp",
    "prettier",

    -- odoo stuffs
    "pyright",
    "yamlls",
    "autopep8",
  },
}

-- git support in nvimtree
M.nvimtree = {
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
    side = "left",
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
        git = true,
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
M.gitsigs = {
  current_line_blame = true,
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
}

return M
