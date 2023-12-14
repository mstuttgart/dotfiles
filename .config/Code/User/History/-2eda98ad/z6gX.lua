-- A high-performance color highlighter
local plugin = {
    "norcalli/nvim-colorizer.lua",
    event = "VeryLazy",
    config = function()
        require("colorizer").setup({ "css", "javascript", "lua", "vim", "toml", "svelte", "typescript", "conf" }, {
            RGB = true,          -- #RGB hex codes
            RRGGBB = true,       -- #RRGGBB hex codes
            names = false,       -- "Name" codes like Blue oe blue
            RRGGBBAA = true,     -- #RRGGBBAA hex codes
            rgb_fn = true,       -- CSS rgb() and rgba() functions
            hsl_fn = true,       -- CSS hsl() and hsla() functions
            css = true,          -- Enable all CSS features: rgb_fn, hsl_fn, names, RGB, RRGGBB
            css_fn = true,       -- Enable all CSS *functions*: rgb_fn, hsl_fn
            -- Available modes: foreground, background, virtualtext
            mode = "background", -- Set the display mode.)
        })
    end,
}

return plugin
