-- Install lazy.nvim automatically

local function echo(str)
    vim.cmd "redraw"
    vim.api.nvim_echo({ { str, "Bold" } }, true, {})
end

echo("  Installing lazy.nvim & plugins ...")

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not vim.loop.fs_stat(lazypath) then
    -- bootstrap lazy.nvim
    -- stylua: ignore
    vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable",
        lazypath })
end

vim.opt.rtp:prepend(vim.env.LAZY or lazypath)

-- require("lazy").setup({
--     spec = {
--       -- add LazyVim and import its plugins
--       { "LazyVim/LazyVim", import = "lazyvim.plugins" },
--       -- import any extras modules here
--       -- { import = "lazyvim.plugins.extras.lang.typescript" },
--       -- { import = "lazyvim.plugins.extras.lang.json" },
--       -- { import = "lazyvim.plugins.extras.ui.mini-animate" },
--       -- import/override with your plugins
--       { import = "plugins" },
--     },
--     defaults = {
--       -- By default, only LazyVim plugins will be lazy-loaded. Your custom plugins will load during startup.
--       -- If you know what you're doing, you can set this to `true` to have all your custom plugins lazy-loaded by default.
--       lazy = false,
--       -- It's recommended to leave version=false for now, since a lot the plugin that support versioning,
--       -- have outdated releases, which may break your Neovim install.
--       version = false, -- always use the latest git commit
--       -- version = "*", -- try installing the latest stable version for plugins that support semver
--     },
--     install = { colorscheme = { "tokyonight", "habamax" } },
--     checker = { enabled = true }, -- automatically check for plugin updates
--     performance = {
--       rtp = {
--         -- disable some rtp plugins
--         disabled_plugins = {
--           "gzip",
--           -- "matchit",
--           -- "matchparen",
--           -- "netrwPlugin",
--           "tarPlugin",
--           "tohtml",
--           "tutor",
--           "zipPlugin",
--         },
--       },
--     },
--   })
  

local opts = {
    ui = {
        custom_keys = { false },
    },
    install = {
        colorscheme = { 'everforest' },
        -- install missing plugins on startup. This doesn't increase startup time.
        missing = true,
    },
    defaults = {
        lazy = false,
        -- It's recommended to leave version=false for now, since a lot the plugin that support versioning,
        -- have outdated releases, which may break your Neovim install.
        version = false, -- always use the latest git commit
    },
    performance = {
        rtp = {
            disabled_plugins = {
                "2html_plugin",
                "bugreport",
                "compiler",
                "ftplugin",
                "getscript",
                "getscriptPlugin",
                "gzip",
                "logipat",
                "matchit",
                "netrw",
                "netrwFileHandlers",
                "netrwPlugin",
                "netrwSettings",
                "optwin",
                "rplugin",
                "rrhelper",
                "spellfile_plugin",
                "synmenu",
                "syntax",
                "tar",
                "tarPlugin",
                "tohtml",
                "tutor",
                "vimball",
                "vimballPlugin",
                "zip",
                "zipPlugin",
            },
        },
    },
    checker = {
        enabled = true,
    },
    debug = false,
}

-- -- Load the plugins and options
require('lazy').setup({ { import = "plugins" } }, opts)
