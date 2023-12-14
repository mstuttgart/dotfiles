-- Install lazy.nvim automatically
local M = {}

M.opts = {
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

-- nget from nvim-chad
local function echo(str)
    vim.cmd "redraw"
    vim.api.nvim_echo({ { str, "Bold" } }, true, {})
end

-- get from https://github.com/NvChad/ui/blob/v2.0/lua/nvchad/post_install.lua#L63
local function show_mason()
    vim.api.nvim_buf_delete(0, { force = true }) -- close previously opened lazy window

    vim.schedule(function()
        vim.cmd "MasonInstallAll"
        -- vim.cmd "MasonInstall "
        -- vim.cmd 'MasonToolsInstall'

        -- Keep track of which mason pkgs get installed
        local packages = table.concat(vim.g.mason_binaries_list, " ")

        require("mason-registry"):on("package:install:success", function(pkg)
            packages = string.gsub(packages, pkg.name:gsub("%-", "%%-"), "") -- rm package name

            -- run above screen func after all pkgs are installed.
            -- if packages:match "%S" == nil then
            --     vim.schedule(function()
            --         vim.api.nvim_buf_delete(0, { force = true })
            --         vim.cmd "echo '' | redraw" -- clear cmdline
            --         -- screen()
            --     end)
            -- end
        end)
    end)
end

M.install_lazy = function()
    echo("  Let's install lazy.nvim & plugins ...")

    local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

    if not vim.loop.fs_stat(lazypath) then
        -- bootstrap lazy.nvim
        -- stylua: ignore
        vim.fn.system({ "git", "clone", "--filter=blob:none", "https://github.com/folke/lazy.nvim.git", "--branch=stable",
            lazypath })
    end

    vim.opt.rtp:prepend(vim.env.LAZY or lazypath)

    -- -- Load the plugins and options
    require('lazy').setup("plugins", M.opts)

    -- show mason install scree

    -- show_mason()
end

return M
