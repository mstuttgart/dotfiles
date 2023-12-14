-- indent blankline settings

local plugin = {
  'lukas-reineke/indent-blankline.nvim',
  version = "2.20.7",
  event = { "BufReadPre", "BufNewFile" },
  dependencies = {
    'nvim-treesitter/nvim-treesitter',
  },
  opts = {
    char = '┆',
    use_treesitter = true,
    show_current_context = true,
  },
}

return plugin
