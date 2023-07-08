-- configure 'plug-n-play' plugins

return {
  -- colorschemes
  { 'Shatur/neovim-ayu',        lazy = true },
  { 'navarasu/onedark.nvim',    lazy = true },
  { 'neanias/everforest-nvim',  priority = 1000 },
  { "Tsuzat/NeoSolarized.nvim", lazy = true },
  {
    'catppuccin/nvim',
    lazy = true,
    name = 'catppuccin',
  },

  {
    'folke/tokyonight.nvim',
    lazy = false,
    opts = {},
  },

  -- {
  --     'karb94/neoscroll.nvim',
  --     config = true,
  -- },

  -- auto close chars like '(', '{', '[' and ''
  {
    'windwp/nvim-autopairs',
    config = true,
  },

  -- comment code
  {
    'echasnovski/mini.comment',
    version = false,
    config = true,
    event = 'VeryLazy',
    opts = {},
  },

  -- highlight for color code
  {
    'norcalli/nvim-colorizer.lua',
    config = function()
      require('colorizer').setup(nil, { css = true })
    end,
  },

  -- Useful plugin to show you pending keybinds.
  {
    'folke/which-key.nvim',
    opts = {},
    lazy = true,
  },

  -- navic complement to breadcumbs
  {
    'utilyre/barbecue.nvim',
    version = '*',
    dependencies = {
      'SmiteshP/nvim-navic',
      'nvim-tree/nvim-web-devicons',
    },
    config = true,
  },

  -- markdown preview :MarkdownPreviewToggle
  {
    'iamcco/markdown-preview.nvim',
    build = function()
      vim.fn['mkdp#util#install']()
    end,
  },

  -- better vim.ui
  {
    'stevearc/dressing.nvim',
    opts = {},
    event = 'VeryLazy',
  },

  -- csv highlight
  {
    'mechatroner/rainbow_csv',
  },
}