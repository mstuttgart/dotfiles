-- telescope settings
local status, telescope = pcall(require, 'telescope')

if (not status) then return end

-- navigate buffers and repos
vim.keymap.set('n', '<leader>ff', '<cmd>Telescope find_files<CR>', ns)

vim.keymap.set('n', '<leader>fg', '<cmd>Telescope live_grep<CR>', ns)

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
