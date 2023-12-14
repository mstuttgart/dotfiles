require("nvim-treesitter.configs").setup {
  -- Add languages to be installed here that you want installed for treesitter
  ensure_installed = { 'lua', 'python', 'markdown', 'javascript', 'html', 'css', 'bash', 'yaml' },
  -- Autoinstall languages that are not installed. Defaults to false (but you can change for yourself!)
  auto_install = true,
  highlight = {
    enable = true,
    use_languagetree = true, },
  indent = {
    enable = true,
    disable = { 'python' },
  },
  context_commentstring = {
    enable = false,
    enable_autocmd = false,
    config = {
      python = '# %s',
    },
  },
}
