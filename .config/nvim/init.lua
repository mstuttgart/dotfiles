-- import modules
require('core.options')
require('core.keymaps')
require('core.autocommands')
require('core.bootstrap')

-- active colorscheme
-- pcall(vim.cmd.colorscheme, 'catppuccin')
pcall(vim.cmd.colorscheme, 'everforest')
-- pcall(vim.cmd.colorscheme, 'ayu')
-- -- pcall(vim.cmd.colorscheme, 'gruvbox-baby')
-- -- pcall(vim.cmd.colorscheme, 'NeoSolarized')
-- -- pcall(vim.cmd.colorscheme, 'nord')
-- --

if vim.g.neovide then
    vim.g.neovide_theme = 'auto'
    vim.g.neovide_cursor_antialiasing = true

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

    -- Helper function for transparency formatting
    local alpha = function()
        return string.format('%x', math.floor(255 * vim.g.transparency or 0.8))
    end
    -- g:neovide_transparency should be 0 if you want to unify transparency of content and title bar.
    vim.g.neovide_transparency = 0.0
    vim.g.transparency = 0.9
    vim.g.neovide_background_color = '#0f1117' .. alpha()

    vim.g.neovide_transparency = 0.9
end
