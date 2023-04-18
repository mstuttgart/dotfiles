-- indent blank setting
vim.opt.list = true

require('indent_blankline').setup {
    char = '┆',
    show_end_of_line = true,
    space_char_blankline = ' ',
}
