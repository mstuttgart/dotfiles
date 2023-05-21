-- indent blankline settings

local plugin = {
  'lukas-reineke/indent-blankline.nvim',
  dependencies = {
    'nvim-treesitter/nvim-treesitter',
  },
  opts = {
    char = '┆',
    show_trailing_blankline_indent = false,
    show_first_indent_level = false,
    use_treesitter = true,
    show_current_context = true,
    show_end_of_line = true,
    space_char_blankline = ' ',
  },
}

return plugin
