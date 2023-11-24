-- Git integration for buffers
local plugin = {
    "lewis6991/gitsigns.nvim",
    opts = {
        current_line_blame = false,
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
        on_attach = function(bufnr)
            local gs = package.loaded.gitsigns

            local function map(mode, l, r, desc)
                vim.keymap.set(mode, l, r, { buffer = bufnr, desc = desc })
            end

            map("n", "<leader>gb", function()
                gs.blame_line { full = true }
            end, "Blame Line")
            map("n", "<leader>gt", gs.toggle_current_line_blame, "Toogle Blame Line")
            map("n", "<leader>gd", gs.diffthis, "Diff This")
            map("n", "<leader>gD", function()
                gs.diffthis "~"
            end, "Diff This ~")
        end,
    },
}

return plugin
