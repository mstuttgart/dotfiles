-- comment
local plugin = {
    "echasnovski/mini.comment",
    version = "*",
    event = "VeryLazy",
    opts = {},
    config = function()
        require("mini.comment").setup {
            options = {
                -- Whether to ignore blank lines
                ignore_blank_line = true,
            },
        }
    end,
}

return plugin
