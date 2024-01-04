-- Git integration for buffers
local plugin = {
  "lewis6991/gitsigns.nvim",
  event = { "BufReadPre", "BufNewFile" },
  config = function()
    require("gitsigns").setup {
      yadm = {
        enable = true,
      },
      on_attach = function(bufnr)
        local gs = package.loaded.gitsigns

        local function map(mode, l, r, opts)
          opts = opts or {}
          opts.buffer = bufnr
          vim.keymap.set(mode, l, r, opts)
        end

        -- Actions
        map("n", "<leader>gt", function()
          gs.blame_line { full = true }
        end, { desc = "Toogle Git Blame" })
        map("n", "<leader>gd", gs.diffthis, { desc = "Diff This" })
      end,
    }
  end,
}

return plugin
