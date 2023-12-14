-- colorschemes

local plugins = {
    {
        'Shatur/neovim-ayu',
        lazy = true,
    },
    {
        'navarasu/onedark.nvim',
        lazy = true,
    },
    -- {
    --     'sainnhe/everforest',
    --     priority=1000,
    --     lazy = false,
    -- },

    {
        "neanias/everforest-nvim",
        version = false,
        lazy = false,
        priority = 1000, -- make sure to load this before all the other start plugins
        -- Optional; default configuration will be used if setup isn't called.
        -- config = function()
        --   require("everforest").setup({
        --     -- Your config here
        --   })
        -- end,
      },

}

return plugins
