-- telescope settings
local status, telescope = pcall(require, 'telescope')

if (not status) then return end

local builtin = require('telescope.builtin')

-- navigate buffers and repos
vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
vim.keymap.set('n', '<leader>fs', builtin.grep_string, {})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})

telescope.setup({
  pickers = {
    find_files = {
      hidden = true
    },
    live_grep = {
      additional_args = function(opts)
        return { "--hidden" }
      end
    },
  },
})

-- load plugins
require('telescope').load_extension('fzf')
