-- import modules
require('core.options')
require('core.keymaps')
require('core.autocommands')
require('core.bootstrap')

-- active colorscheme
-- pcall(vim.cmd.colorscheme, 'catppuccin-latte')
pcall(vim.cmd.colorscheme, 'everforest')
-- pcall(vim.cmd.colorscheme, 'NeoSolarized')
-- pcall(vim.cmd.colorscheme, 'tokyonight-night')
--
if vim.g.neovide then
    --     -- Put anything you want to happen only in Neovide here
    vim.o.guifont = 'JetBrainsMono Nerd Font:h12' -- text below applies for VimScript
    --
    vim.g.neovide_scale_factor = 1.0
    local change_scale_factor = function(delta)
        vim.g.neovide_scale_factor = vim.g.neovide_scale_factor * delta
    end
    vim.keymap.set('n', '<C-=>', function()
        change_scale_factor(1.25)
    end)
    vim.keymap.set('n', '<C-->', function()
        change_scale_factor(1 / 1.25)
    end)
end
