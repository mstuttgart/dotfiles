-- configure autocomplete
local plugins = {
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

    -- loads vscode style snippets from installed plugins (e.g. friendly-snippets)
    require("luasnip.loaders.from_vscode").lazy_load()

    cmp.setup {
      completion = {
        keyword_length = 2,
        completeopt = "menu,menuone,preview,noselect",
      },
      snippet = {   -- configure how nvim-cmp interacts with snippet engine
        expand = function(args)
          luasnip.lsp_expand(args.body)
        end,
      },
      mapping = cmp.mapping.preset.insert {
        ["<C-n>"] = cmp.mapping.select_next_item { behavior = cmp.SelectBehavior.Insert },
        ["<C-p>"] = cmp.mapping.select_prev_item { behavior = cmp.SelectBehavior.Insert },
        ["<C-k>"] = cmp.mapping.scroll_docs(-4),
        ["<C-j>"] = cmp.mapping.scroll_docs(4),
        ["<C-Space>"] = cmp.mapping.complete(),   -- show completion suggestions
        ["<C-e>"] = cmp.mapping.abort(),          -- close completion window
        ["<Esc>"] = cmp.mapping.close(),
        ["<CR>"] = cmp.mapping.confirm { select = false },
      },

      -- sources for autocompletion
      sources = cmp.config.sources {
        { name = "nvim_lsp" },
        { name = "luasnip" },   -- snippets
        { name = "buffer" },    -- text within current buffer
        { name = "path" },      -- file system paths
        { name = "cmdline" },   -- command line
      },
    }
  end,

}

return plugins
