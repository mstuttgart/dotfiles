-- load luasnips + cmp related in insert mode only
local plugins = {
    "hrsh7th/nvim-cmp",
    event = "InsertEnter",
    dependencies = {
        {
            -- snippet plugin
            "L3MON4D3/LuaSnip",
            dependencies = "rafamadriz/friendly-snippets",
            opts = {
                history = true,
                updateevents = "TextChanged,TextChangedI",
            },
            keys = function()
                -- Disable default <tab> and <s-tab> behavior in LuaSnip
                -- to use <tab> in autocomplete
                return {}
            end,
        },

        -- cmp sources plugins
        {
            "saadparwaiz1/cmp_luasnip",
            "hrsh7th/cmp-nvim-lua",
            "hrsh7th/cmp-nvim-lsp",
            "hrsh7th/cmp-buffer",
            "hrsh7th/cmp-path",
        },
    },
    opts = function()
        return require "plugins.configs.cmp"
    end,
    config = function(_, opts)
        require("cmp").setup(opts)
    end,
}

return plugins
