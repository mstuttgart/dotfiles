-- treesitter settings
--
require("nvim-treesitter.configs").setup({
  ensure_installed = {
    'python',
    'javascript',
    'lua',
    'vim',
    'html',
    'css',
    'yaml',
    'bash',
    'markdown',
    'comment',
    'vim',
    'regex',
    'ini',
    'json',
    'po',
    'sql',
  },

  highlight = {
    enable = true,
  },
  indent = {
    enable = true,
  },
  context_commentstring = {
    enable = true,
  },
})
