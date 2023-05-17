-- symbols settings
local status, symbols = pcall(require, 'symbols-outline')

if (not status) then return end

symbols.setup({
  -- change connector color to foreground color
  vim.api.nvim_create_autocmd(
      'BufEnter',
      {
        -- change connector color
        pattern = '*',
        command = 'hi SymbolsOutlineConnector gui=none guifg=vim.g.foreground',
      }
  )
})

-- toogle symbols panel
vim.keymap.set('n',  '<leader>tg', ':SymbolsOutline<CR>', {})
