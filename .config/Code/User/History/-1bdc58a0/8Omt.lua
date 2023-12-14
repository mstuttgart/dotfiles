vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {

  

  -- Find the enemy and replace them with dark power.
  {
    "nvim-pack/nvim-spectre",
    build = false,
    cmd = "Spectre",
    opts = { open_cmd = "noswapfile vnew" },
        -- stylua: ignore
        keys = {
            { "<leader>sr", function() require("spectre").open() end, desc = "Replace in files (Spectre)" },
        },
  },

  -- Find, Filter, Preview, Pick. All lua, all the time.
  {
    "nvim-telescope/telescope.nvim",
    branch = "0.1.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      {
        "nvim-telescope/telescope-fzf-native.nvim",
        build = "make",
      },
    },
    keys = {
      -- git
      { "<leader>gc", "<cmd>Telescope git_commits<CR>", desc = "commits" },
      { "<leader>gs", "<cmd>Telescope git_status<CR>", desc = "status" },
    },
    config = function()
      require("telescope").setup {
        defaults = {
          preview = {
            treesitter = false,
          },
        },
        extensions = {
          fzf = {
            fuzzy = true, -- false will only do exact matching
            override_generic_sorter = true, -- override the generic sorter
            override_file_sorter = true, -- override the file sorter
            case_mode = "smart_case", -- or "ignore_case" or "respect_case"
          },
        },
      }

      require("telescope").load_extension "fzf"
    end,
    init = function()
      vim.keymap.set("n", "<leader>sf", require("telescope.builtin").find_files, { desc = "Search Files" })
      vim.keymap.set("n", "<leader>sw", require("telescope.builtin").grep_string, { desc = "Search current Word" })
      vim.keymap.set("n", "<leader>sh", require("telescope.builtin").help_tags, { desc = "Search Help" })
      vim.keymap.set("n", "<leader>sg", require("telescope.builtin").live_grep, { desc = "Search by Grep" })
      vim.keymap.set("n", "<leader>ss", require("telescope.builtin").lsp_document_symbols, { desc = "Search Symbols" })
      vim.keymap.set("n", "<leader>sd", require("telescope.builtin").diagnostics, { desc = "Search Diagnostics" })
    end,
  },

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
