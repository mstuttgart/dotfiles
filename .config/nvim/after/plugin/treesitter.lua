-- treesitter settings
local status, treesitter = pcall(require, 'nvim-treesitter.configs')

if (not status) then return end

treesitter.setup({
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
    'vim',
    'ini',
    'json',
    'po',
    'sql',
    'toml',
    'fish',
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
