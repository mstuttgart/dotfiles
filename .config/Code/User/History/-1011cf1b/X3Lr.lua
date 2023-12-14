-- plugin to visualize and operate on indent scope.
local plugin = {
    "echasnovski/mini.indentscope",
    version = false,
    event = {
        "BufReadPre",
        "BufNewFile",
    },
    opts = {
        symbol = "┆",
        options = { try_as_border = true },
    },
    init = function()
        vim.api.nvim_create_autocmd("FileType", {
            pattern = {
                "alpha",
                "dashboard",
                "help",
                "lazy",
                "lazyterm",
                "mason",
                "neo-tree",
                "notify",
                "toggleterm",
                "trouble",
                "Trouble",
            },
            callback = function()
                vim.b.miniindentscope_disable = true
            end,
        })
    end,
}

return plugin
