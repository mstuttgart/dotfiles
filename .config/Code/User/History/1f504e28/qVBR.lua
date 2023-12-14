-- indent blankline settings

local plugin = {
  'lukas-reineke/indent-blankline.nvim',
  version = "2.20.7",
  dependencies = {
    'nvim-treesitter/nvim-treesitter',
  },
  opts = {
    char = '┆',
    use_treesitter = true,
  },
}

return plugin
