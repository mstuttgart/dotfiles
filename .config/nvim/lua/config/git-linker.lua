-- gitlinker basic settings

require('gitlinker').setup({
  mappings = nil, -- disable keymaps
  opts = {
    -- adds current line nr in the url for normal mode
    add_current_line_on_normal_mode = true,
    -- callback for what to do with the url
    action_callback = require"gitlinker.actions".copy_to_clipboard,
    -- print the url after performing the action
    print_url = true,
  },
})

vim.keymap.set({ 'n', 'v' }, "<leader>gl", "", {
  silent = true,
  desc = 'Get git permlink',
  callback = function()
    local mode = string.lower(vim.fn.mode())
    gitlinker.get_buf_range_url(mode)
  end,
})

vim.keymap.set('n', '<leader>gb', '', {
  silent = true,
  desc = 'Browse repo in browser',
  callback = function()
    gitlinker.get_repo_url({
      action_callback = gitlinker.actions.open_in_browser
    })
  end
})
