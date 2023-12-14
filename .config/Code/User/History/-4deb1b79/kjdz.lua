-- load luasnips + cmp related in insert mode only
local plugins = {
    "hrsh7th/nvim-cmp",
    event = "InsertEnter",
    opts = {
        history = true,
        updateevents = "TextChanged,TextChangedI",
    },
    keys = function()
        -- Disable default <tab> and <s-tab> behavior in LuaSnip
        -- to use <tab> in autocomplete
        return {}
    end,
    dependencies = {
        {
            -- snippet plugin
            "L3MON4D3/LuaSnip",
            dependencies = "rafamadriz/friendly-snippets",

        },

        -- cmp sources plugins
        {
            'hrsh7th/cmp-nvim-lsp',
            'hrsh7th/cmp-nvim-lua',
            'hrsh7th/cmp-buffer',
            'hrsh7th/cmp-cmdline',
            'hrsh7th/cmp-path',
            'saadparwaiz1/cmp_luasnip',
            'L3MON4D3/LuaSnip',
            'rafamadriz/friendly-snippets',
        },
    },
    -- opts = function(_, opts)
    --     local has_words_before = function()
    --         unpack = unpack or table.unpack
    --         local line, col = unpack(vim.api.nvim_win_get_cursor(0))
    --         return col ~= 0 and vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
    --     end

    --     local luasnip = require("luasnip")
    --     local cmp = require("cmp")

    --     opts.mapping = vim.tbl_extend("force", opts.mapping, {
    --         ["<Tab>"] = cmp.mapping(function(fallback)
    --             if cmp.visible() then
    --                 -- You could replace select_next_item() with confirm({ select = true }) to get VS Code autocompletion behavior
    --                 cmp.select_next_item()
    --                 -- You could replace the expand_or_jumpable() calls with expand_or_locally_jumpable()
    --                 -- this way you will only jump inside the snippet region
    --             elseif luasnip.expand_or_jumpable() then
    --                 luasnip.expand_or_jump()
    --             elseif has_words_before() then
    --                 cmp.complete()
    --             else
    --                 fallback()
    --             end
    --         end, { "i", "s" }),
    --         ["<S-Tab>"] = cmp.mapping(function(fallback)
    --             if cmp.visible() then
    --                 cmp.select_prev_item()
    --             elseif luasnip.jumpable(-1) then
    --                 luasnip.jump(-1)
    --             else
    --                 fallback()
    --             end
    --         end, { "i", "s" }),
    --     })
    -- end,
    -- config = function(_, opts)
    --     require("cmp").setup(opts)
    -- end,
}

return {}
