vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {

  

  -- Find the enemy and replace them with dark power.
  -- {
  --   "nvim-pack/nvim-spectre",
  --   build = false,
  --   cmd = "Spectre",
  --   opts = { open_cmd = "noswapfile vnew" },
  --       -- stylua: ignore
  --       keys = {
  --           { "<leader>sr", function() require("spectre").open() end, desc = "Replace in files (Spectre)" },
  --       },
  -- },

  

  -- Git integration for buffers
  {
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
  },

  -- see code tags
  {
    "simrat39/symbols-outline.nvim",
    cmd = "SymbolsOutline",
    keys = {
      { "<leader>ct", "<cmd>SymbolsOutline<cr>", desc = "Code Tags (Symbols Outline)" },
    },
    config = function()
      require("symbols-outline").setup {
        vim.api.nvim_create_autocmd("BufEnter", {
          pattern = "*",
          command = "hi SymbolsOutlineConnector gui=none guifg=vim.g.foreground",
        }),
      }
    end,
  },


}

return plugins
