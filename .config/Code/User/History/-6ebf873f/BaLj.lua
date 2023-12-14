-- coding plugins

local plugins = {
  -- snippets engine
  {

    "L3MON4D3/LuaSnip",
    event = "VeryLazy",
  },
  -- snippets collection
  {
    "rafamadriz/friendly-snippets",
    event = "VeryLazy",
  },

  -- highlight for color code
  {
    "norcalli/nvim-colorizer.lua",
    event = "VeryLazy",
    config = function()
      require("colorizer").setup({ "css", "javascript", "lua", "vim", "toml", "svelte", "typescript", "conf" }, {
        RGB = true,          -- #RGB hex codes
        RRGGBB = true,       -- #RRGGBB hex codes
        names = false,       -- "Name" codes like Blue oe blue
        RRGGBBAA = true,     -- #RRGGBBAA hex codes
        rgb_fn = true,       -- CSS rgb() and rgba() functions
        hsl_fn = true,       -- CSS hsl() and hsla() functions
        css = true,          -- Enable all CSS features: rgb_fn, hsl_fn, names, RGB, RRGGBB
        css_fn = true,       -- Enable all CSS *functions*: rgb_fn, hsl_fn
        -- Available modes: foreground, background, virtualtext
        mode = "background", -- Set the display mode.)
      })
    end,
  },

  -- csv highlight
  {
    "mechatroner/rainbow_csv",
    event = "VeryLazy",
  },

  -- word highlight
  {
    "echasnovski/mini.cursorword",
    event = "VeryLazy",
    version = "*",
    config = function()
      require("mini.cursorword").setup()
    end,
  },

  -- comment
  {
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
  },

  -- surround
  {
    "kylechui/nvim-surround",
    version = "*", -- Use for stability; omit to use `main` branch for the latest features
    event = "VeryLazy",
    config = function()
      require("nvim-surround").setup {
        -- Configuration here, or leave empty to use defaults
      }
    end,
  },

  -- add code docs
  {
    "danymat/neogen",
    config = true,
    event = "VeryLazy",
    init = function()
      vim.keymap.set(
        "n",
        "<Leader>cd",
        ':lua require("neogen").generate()<CR>',
        { silent = true, desc = "Generate Documentation" }
      )
    end,
  },

  -- better scape shortcuts
  {
    "max397574/better-escape.nvim",
    event = "InsertEnter",
    config = function()
      require("better_escape").setup()
    end,
  },

  -- install odoo snippets
  {
    "mstuttgart/vscode-odoo-snippets",
    event = "InsertEnter",
    dependencies = {
      "L3MON4D3/LuaSnip",
    },
    config = function()
      require("luasnip.loaders.from_vscode").lazy_load()
    end,
  },

  -- configure linters
  {
    "mfussenegger/nvim-lint",
    event = {
      "BufReadPre",
      "BufNewFile",
    },
    config = function()
      local lint = require "lint"

      lint.linters_by_ft = {
        ansible = { "ansible_lint" },
        bash = { "shellcheck" },
        javascript = { "eslint_d" },
        python = { "pylint" },
        typescript = { "eslint_d" },
      }

      vim.api.nvim_create_autocmd({ "BufWritePost" }, {
        callback = function()
          lint.try_lint()
        end,
      })
    end,
  },

  {
    "nvimtools/none-ls.nvim",
    lazy = true,
    -- event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      "jay-babu/mason-null-ls.nvim",
    },
    init = function()
      vim.keymap.set("n", "<leader>cf", vim.lsp.buf.format, { desc = "Format File" })
    end,
    opts = function()
      local nls = require "null-ls"
      return {
        root_dir = require("null-ls.utils").root_pattern(".null-ls-root", ".neoconf.json", "Makefile", ".git"),
        sources = {
          nls.builtins.formatting.shfmt,
          nls.builtins.formatting.stylua,
          nls.builtins.formatting.isort,
          nls.builtins.formatting.autopep8,
          nls.builtins.formatting.xmlformat.with {
            arg = { "--blanks", "--indent 4" },
          },
          nls.builtins.formatting.xmllint.with {
            { "--format", "-" },
          },
          nls.builtins.formatting.yamlfmt,
          nls.builtins.formatting.prettier.with {
            prefer_local = "node_modules/.bin",
          },
          nls.builtins.formatting.eslint.with {
            prefer_local = "node_modules/.bin",
          },
          nls.builtins.diagnostics.pylint.with {
            diagnostic_config = { underline = false, virtual_text = false, signs = true },
            prefer_local = ".venv/bin",
          },
          nls.builtins.diagnostics.ansiblelint,
          nls.builtins.diagnostics.eslint.with {
            prefer_local = "node_modules/.bin",
          },
          nls.builtins.diagnostics.shellcheck,
          nls.builtins.code_actions.eslint.with {
            prefer_local = "node_modules/.bin",
          },
        },
      }
    end,
  },

  -- Configure mason to autoinstall linters and formatters
  {
    "williamboman/mason.nvim",
    dependencies = {
      "williamboman/mason-lspconfig.nvim",
      "WhoIsSethDaniel/mason-tool-installer.nvim",
    },
    cmd = { "Mason", "MasonInstall", "MasonInstallAll", "MasonUpdate" },
    config = function()
      require("mason").setup {
        ui = {
          icons = {
            package_installed = "✓",
            package_pending = "➜",
            package_uninstalled = "✗",
          },
        },
      }

      -- auto install LSP
      require("mason-lspconfig").setup {
        ensure_installed = {
          "pyright",
          "html",
          "cssls",
          "lua_ls",
          "bashls",
          "ansiblels",
        },
        -- auto-install configured servers (with lspconfig)
        automatic_installation = true, -- not the same as ensure_installed
      }

      require("mason-tool-installer").setup {
        ensure_installed = {
          -- linters
          "eslint_d",
          "shellcheck",
          "pylint",

          -- formatters
          "autopep8",
          "isort",
          "prettier",
          "shfmt",
          "stylua",
          "xmlformatter",
          "yamlfmt",
        },
      }
    end,
  },

  -- condfigure autocomplete
  {
    "hrsh7th/nvim-cmp",
    event = "InsertEnter",
    dependencies = {
      -- autocomplete plugins
      "hrsh7th/cmp-buffer",
      "hrsh7th/cmp-path",
      "hrsh7th/cmp-cmdline",

      -- snippet autocomplete and engine
      "L3MON4D3/LuaSnip",
      "saadparwaiz1/cmp_luasnip",
      "rafamadriz/friendly-snippets",

      -- vscode like icons to autocomplete list
      "onsails/lspkind.nvim",
    },
    config = function()
      local cmp = require "cmp"
      local luasnip = require "luasnip"
      local lspkind = require "lspkind"

      -- loads vscode style snippets from installed plugins (e.g. friendly-snippets)
      require("luasnip.loaders.from_vscode").lazy_load()

      local has_words_before = function()
        unpack = unpack or table.unpack
        local line, col = unpack(vim.api.nvim_win_get_cursor(0))
        return col ~= 0 and vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match "%s" == nil
      end

      cmp.setup {
        completion = {
          keyword_length = 1,
          completeopt = "menu,menuone,preview,noselect",
        },
        snippet = { -- configure how nvim-cmp interacts with snippet engine
          expand = function(args)
            luasnip.lsp_expand(args.body)
          end,
        },
        mapping = cmp.mapping.preset.insert {
          -- ["<C-n>"] = cmp.mapping.select_next_item { behavior = cmp.SelectBehavior.Insert },
          -- ["<C-p>"] = cmp.mapping.select_prev_item { behavior = cmp.SelectBehavior.Insert },
          ["<C-k>"] = cmp.mapping.scroll_docs(-4),
          ["<C-j>"] = cmp.mapping.scroll_docs(4),
          ["<C-Space>"] = cmp.mapping.complete(), -- show completion suggestions
          ["<C-e>"] = cmp.mapping.abort(),        -- close completion window
          ["<Esc>"] = cmp.mapping.close(),
          ["<CR>"] = cmp.mapping.confirm { select = false },
          ["<Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_next_item()
              -- You could replace the expand_or_jumpable() calls with expand_or_locally_jumpable()
              -- that way you will only jump inside the snippet region
            elseif has_words_before() then
              cmp.complete()
            elseif luasnip.expand_or_jumpable() then
              luasnip.expand_or_jump()
            else
              fallback()
            end
          end, { "i", "s" }),
          ["<S-Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_prev_item()
            elseif luasnip.jumpable(-1) then
              luasnip.jump(-1)
            else
              fallback()
            end
          end, { "i", "s" }),
        },

        -- sources for autocompletion
        sources = cmp.config.sources {
          { name = "nvim_lsp" },
          { name = "luasnip" }, -- snippets
          { name = "buffer" },  -- text within current buffer
          { name = "path" },    -- file system paths
          { name = "cmdline" }, -- command line
        },
      }
    end,
  },

  -- autopairing of (){}[] etc
  {
    "windwp/nvim-autopairs",
    opts = {
      fast_wrap = {},
      disable_filetype = { "TelescopePrompt", "vim" },
    },
    config = function(_, opts)
      require("nvim-autopairs").setup(opts)

      -- setup cmp for autopairs
      local cmp_autopairs = require "nvim-autopairs.completion.cmp"
      require("cmp").event:on("confirm_done", cmp_autopairs.on_confirm_done())
    end,
  },
}

return plugins
