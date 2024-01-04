-- Find, Filter, Preview, Pick. All lua, all the time.
local plugins = {
  "nvim-telescope/telescope.nvim",
  branch = "0.1.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    {
      "nvim-telescope/telescope-fzf-native.nvim",
      build = "make",
    },
    {
      "nvim-telescope/telescope-live-grep-args.nvim",
      -- This will not install any breaking changes.
      -- For major updates, this must be adjusted manually.
      version = "^1.0.0",
    },
  },
  keys = {
    -- git
    { "<leader>gc", "<cmd>Telescope git_commits<CR>", desc = "commits" },
    { "<leader>gs", "<cmd>Telescope git_status<CR>",  desc = "status" },
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
          fuzzy = true,                   -- false will only do exact matching
          override_generic_sorter = true, -- override the generic sorter
          override_file_sorter = true,    -- override the file sorter
          case_mode = "smart_case",       -- or "ignore_case" or "respect_case"
        },
      },
    }

    require("telescope").load_extension "fzf"
    require("telescope").load_extension "live_grep_args"
  end,
  init = function()
    vim.keymap.set("n", "<leader>sf", require("telescope.builtin").find_files, { desc = "Search Files" })
    vim.keymap.set("n", "<leader>sw", require("telescope.builtin").grep_string, { desc = "Search current Word" })
    vim.keymap.set("n", "<leader>sh", require("telescope.builtin").help_tags, { desc = "Search Help" })
    vim.keymap.set("n", "<leader>sg", require("telescope").extensions.live_grep_args.live_grep_args, { desc = "Search by Grep" })
    vim.keymap.set("n", "<leader>ss", require("telescope.builtin").lsp_document_symbols, { desc = "Search Symbols" })
    vim.keymap.set("n", "<leader>sd", require("telescope.builtin").diagnostics, { desc = "Search Diagnostics" })
  end,
}

return plugins
