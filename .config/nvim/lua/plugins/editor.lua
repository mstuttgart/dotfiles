vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

local plugins = {

  -- A file explorer tree for neovim written in lua
  {
    "nvim-tree/nvim-tree.lua",
    -- lazy = true,
    cmd = { "NvimTreeToggle", "NvimTreeFocus" },
    dependencies = {
      "nvim-tree/nvim-web-devicons",
    },
    keys = {
      { "<leader>ee", "<cmd> NvimTreeFocus <CR>", desc = "Focus nvimtree" },
      { "<leader>et", "<cmd> NvimTreeToggle <CR>", desc = "Toogle nvimtree" },
      { "<leader>ef", "<cmd> NvimTreeFindFile <CR>", desc = "nvimtree open with current File" },
      { "<leader>er", "<cmd> NvimTreeRefresh <CR>", desc = "nvimtree Refresh" },
      { "<leader>ec", "<cmd> NvimTreeCollapse<CR>", desc = "Collapse file explorer" },
    },
    opts = {
      filters = {
        dotfiles = false,
        custom = { "^\\.git", "__pycache__" },
      },
      disable_netrw = true,
      hijack_netrw = true,
      hijack_cursor = true,
      hijack_unnamed_buffer_when_opening = false,
      sync_root_with_cwd = true,
      update_focused_file = {
        enable = true,
        update_root = false,
      },
      view = {
        adaptive_size = true,
        side = "left",
        width = 30,
        preserve_window_proportions = true,
      },
      git = {
        enable = true, -- show git statuses
        ignore = false, -- still show .gitignored files
        show_on_dirs = true,
        show_on_open_dirs = true,
        timeout = 400,
      },
      filesystem_watchers = {
        enable = true,
      },
      actions = {
        open_file = {
          resize_window = true,
        },
      },
      renderer = {
        root_folder_label = false,
        highlight_git = false,
        highlight_opened_files = "none",
        indent_markers = {
          enable = true,
          icons = {
            corner = "└ ",
            edge = "┆ ",
            item = "┆ ",
            none = "  ",
          },
        },
        icons = {
          webdev_colors = false,
          show = {
            file = true,
            folder = true,
            folder_arrow = false,
            git = false,
          },
          glyphs = {
            default = "",
            symlink = "",
            folder = {
              arrow_closed = "",
              arrow_open = "",
              default = "",
              open = "",
              empty = "",
              empty_open = "",
              symlink = "",
              symlink_open = "",
            },
            git = {
              unstaged = "",
              staged = "",
              unmerged = "",
              renamed = "➜",
              untracked = "",
              deleted = "",
              ignored = "◌",
            },
          },
        },
      },
    },
    init = function()
      -- add theme to nvim-tree background1
      vim.cmd "autocmd Colorscheme * highlight NvimTreeNormal guibg=NONE ctermbg=NONE"
      vim.cmd "autocmd Colorscheme * highlight NvimTreeEndOfBuffer guibg=NONE ctermbg=NONE"
    end,
    config = function(_, opts)
      require("nvim-tree").setup(opts)
    end,
  },

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
      "nvim-tree/nvim-tree.lua",
      {
        "nvim-telescope/telescope-fzf-native.nvim",
        build = "make",
      },
      { "nvim-telescope/telescope-live-grep-args.nvim" },
    },
    keys = {
      -- git
      { "<leader>gc", "<cmd>Telescope git_commits<CR>", desc = "commits" },
      { "<leader>gs", "<cmd>Telescope git_status<CR>", desc = "status" },
    },
    config = function()
      require("telescope").load_extension "fzf"
      require("telescope").load_extension "live_grep_args"
    end,
    init = function()
      vim.keymap.set("n", "<leader>sf", require("telescope.builtin").find_files, { desc = "Search Files" })
      vim.keymap.set("n", "<leader>sw", require("telescope.builtin").grep_string, { desc = "Search current Word" })
      vim.keymap.set("n", "<leader>sh", require("telescope.builtin").help_tags, { desc = "[S]earch [H]elp" })
      vim.keymap.set("n", "<leader>sw", require("telescope.builtin").grep_string, { desc = "[S]earch current [W]ord" })
      vim.keymap.set("n", "<leader>sg", require("telescope").extensions.live_grep_args.live_grep_args, { desc = "[S]earch by [G]rep" })
      vim.keymap.set("n", "<leader>sd", require("telescope.builtin").diagnostics, { desc = "[S]earch [D]iagnostics" })
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

  -- terminal emulator
  {
    "NvChad/nvterm",
    config = function()
      require("nvterm").setup()
    end,
    init = function()
      vim.keymap.set({ "n", "t" }, "<leader>;", function()
        require("nvterm.terminal").toggle "horizontal"
      end, { silent = true })
    end,
  },

  -- Seamless navigation between tmux panes and vim splits
  {
    "christoomey/vim-tmux-navigator",
  },
}

return plugins
