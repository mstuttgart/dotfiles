-- treesitter settings
-- Highlight, edit, and navigate code

local plugin = {
  'nvim-treesitter/nvim-treesitter',
  dependencies = {
    'nvim-treesitter/nvim-treesitter-textobjects',
    "windwp/nvim-ts-autotag",
    -- extra extra textobjects
    {
      "chrisgrieser/nvim-various-textobjs",
      config = function() require("various-textobjs").setup({ useDefaultKeymaps = true }) end,
    },
  },
  build = ':TSUpdate',
  config = function()
    require('nvim-treesitter.configs').setup {
      -- Add languages to be installed here that you want installed for treesitter
      ensure_installed = { 'lua', 'python', 'markdown', 'javascript', 'fish', 'html', 'css', 'bash', 'yaml' },
      -- Autoinstall languages that are not installed. Defaults to false (but you can change for yourself!)
      auto_install = true,
      highlight = { enable = true },
      indent = { enable = true, disable = { 'python' } },
      context_commentstring = {
        enable = true,
        enable_autocmd = false,
        config = {
          python = '# %s',
        },
      },
    }
  end
}

return plugin
