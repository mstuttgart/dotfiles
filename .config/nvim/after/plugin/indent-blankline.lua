-- indent-blankline settings
local status, blankline = pcall(require, 'indent_blankline')

if (not status) then return end

-- indent blank setting
vim.opt.list = true

blankline.setup {
    char = '┆',
    show_end_of_line = true,
    space_char_blankline = ' ',
}
