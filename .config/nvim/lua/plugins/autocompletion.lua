-- autocomplete settings

local plugin = {
  -- Autocompletion
  'hrsh7th/nvim-cmp',
  dependencies = {
    -- completion sources
    'hrsh7th/cmp-nvim-lsp',
    'hrsh7th/cmp-nvim-lsp-signature-help',
    'hrsh7th/cmp-nvim-lua',
    'hrsh7th/cmp-buffer',
    'saadparwaiz1/cmp_luasnip',
    'hrsh7th/cmp-path',
    'L3MON4D3/LuaSnip',
    'rafamadriz/friendly-snippets',
    -- complements
    'onsails/lspkind-nvim', -- add the nice source + completion item kind to the menu
  },
  config = function()
    local cmp = require('cmp')
    local luasnip = require 'luasnip'

    require('luasnip.loaders.from_vscode').lazy_load()
    luasnip.config.setup {}

    cmp.setup({
      snippet = {
        expand = function(args) require('luasnip').lsp_expand(args.body) end,
      },
      sources = cmp.config.sources({
        { name = 'luasnip' },
        { name = 'nvim_lsp_signature_help' },
        { name = 'nvim_lua' },
        { name = 'nvim_lsp' },
        { name = 'path' },
        { name = 'buffer',                 keyword_length = 3 }, -- don't complete from buffer right away
      }),
      mapping = cmp.mapping.preset.insert({
        ['<C-f>'] = cmp.mapping.scroll_docs(-4),
        ['<C-d>'] = cmp.mapping.scroll_docs(4),
        ['<C-h>'] = cmp.mapping.complete({ reason = cmp.ContextReason.Manual }),
        ['<C-e>'] = cmp.mapping.abort(),
        ['<C-y>'] = cmp.mapping.confirm({
          behavior = cmp.ConfirmBehavior.Insert,
          select = true, -- use first result if none explicitly selected
        }),
        ['<C-n>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Select }),
        ['<C-p>'] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Select }),
        ['<Tab>'] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_next_item()
          elseif luasnip.expand_or_locally_jumpable() then
            luasnip.expand_or_jump()
          else
            fallback()
          end
        end, { 'i', 's' }),
      }),
      preselect = cmp.PreselectMode.Item, -- auto select whatever entry the source says
      formatting = {
        -- Show where the completion opts are coming from
        format = require('lspkind').cmp_format({
          with_text = true,
          menu = {
            luasnip = '[snippet]',
            nvim_lua = '[nvim]',
            nvim_lsp = '[LSP]',
            path = '[path]',
            buffer = '[buffer]',
            nvim_lsp_signature_help = '[param]',
          },
        }),
      },
    })
  end,
}

return plugin
