-- formatting , linting
local plugin = {
    "stevearc/conform.nvim",
    lazy = true,
    config = function()
        require "plugins.configs.conform"
    end,
}


return plugin
