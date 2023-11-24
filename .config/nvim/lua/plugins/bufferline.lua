-- A snazzy bufferline for Neovim
local plugin = {
    "akinsho/bufferline.nvim",
    dependencies = {
        { "echasnovski/mini.bufremove", version = "*" },
    },
    event = "VeryLazy",
    keys = {
        { "<leader>bQ", "<Cmd>BufferLineGroupClose ungrouped<CR>", desc = "Delete non-pinned buffers" },
        { "<leader>bo", "<Cmd>BufferLineCloseOthers<CR>",          desc = "Delete other buffers" },
        { "<leader>br", "<Cmd>BufferLineCloseRight<CR>",           desc = "Delete buffers to the right" },
        { "<leader>bl", "<Cmd>BufferLineCloseLeft<CR>",            desc = "Delete buffers to the left" },
        { "<Tab>",      "<cmd>BufferLineCyclePrev<cr>",            desc = "Prev buffer" },
        { "<S-Tab>",    "<cmd>BufferLineCycleNext<cr>",            desc = "Next buffer" },
    },
    opts = {
        options = {
            close_command = function(n)
                require("mini.bufremove").delete(n, false)
            end,
            right_mouse_command = function(n)
                require("mini.bufremove").delete(n, false)
            end,
            diagnostics = "nvim_lsp",
            separator_style = "thin",
            always_show_bufferline = true,
            offsets = {
                {
                    filetype = "NvimTree",
                    text = "",
                    highlight = "Directory",
                    text_align = "left",
                    separator = false,
                },
            },
        },
    },
}

return plugin
