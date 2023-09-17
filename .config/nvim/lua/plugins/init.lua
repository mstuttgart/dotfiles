-- configure 'plug-n-play' plugins

return {
    -- colorschemes
    { 'Shatur/neovim-ayu', lazy = true },
    { 'navarasu/onedark.nvim', lazy = true },
    {
        'luisiacc/gruvbox-baby',
        lazy = true,
    },
    {
        'EdenEast/nightfox.nvim',
        lazy = true,
        config = function()
            require('nightfox').setup {
                options = {
                    transparent = true,
                },
                styles = {
                    comments = 'italic',
                    keywords = 'bold',
                    types = 'italic,bold',
                },
            }
        end,
    },
    { 'shaunsingh/nord.nvim' },
    {
        'neanias/everforest-nvim',
        priority = 1000,
        config = function()
            require('everforest').setup {
                ---Controls the "hardness" of the background. Options are "soft", "medium" or "hard".
                ---Default is "medium".
                background = 'medium',
                ---How much of the background should be transparent. 2 will have more UI
                ---components be transparent (e.g. status line background)
                transparent_background_level = 1,
                ---Whether italics should be used for keywords and more.
                italics = false,
                ---Disable italic fonts for comments. Comments are in italics by default, set
                ---this to `true` to make them _not_ italic!
                disable_italic_comments = false,
                ---By default, the colour of the sign column background is the same as the as normal text
                ---background, but you can use a grey background by setting this to `"grey"`.
                sign_column_background = 'none',
                ---The contrast of line numbers, indent lines, etc. Options are `"high"` or
                ---`"low"` (default).
                ui_contrast = 'low',
                ---Dim inactive windows. Only works in Neovim. Can look a bit weird with Telescope.
                dim_inactive_windows = false,
                ---Some plugins support highlighting error/warning/info/hint texts, by
                ---default these texts are only underlined, but you can use this option to
                ---also highlight the background of them.
                diagnostic_text_highlight = false,
                ---Which colour the diagnostic text should be. Options are `"grey"` or `"coloured"` (default)
                diagnostic_virtual_text = 'coloured',
                ---Some plugins support highlighting error/warning/info/hint lines, but this
                ---feature is disabled by default in this colour scheme.
                diagnostic_line_highlight = false,
                ---By default, this color scheme won't colour the foreground of |spell|, instead
                ---colored under curls will be used. If you also want to colour the foreground,
                ---set this option to `true`.
                spell_foreground = false,
                ---You can override specific highlights to use other groups or a hex colour.
                ---This function will be called with the highlights and colour palette tables.
                ---@param highlight_groups Highlights
                ---@param palette Palette
                on_highlights = function(highlight_groups, palette) end, -- Your config here
            }
        end,
    },
    { 'Tsuzat/NeoSolarized.nvim', lazy = true },
    {
        'catppuccin/nvim',
        lazy = true,
        name = 'catppuccin',
    },

    {
        'folke/tokyonight.nvim',
        lazy = false,
        opts = {},
    },

    -- auto close chars like '(', '{', '[' and ''
    {
        'windwp/nvim-autopairs',
        config = true,
    },

    -- comment code
    {
        'echasnovski/mini.comment',
        version = false,
        config = true,
        event = 'VeryLazy',
        opts = {},
    },

    -- highlight for color code
    {
        'norcalli/nvim-colorizer.lua',
        config = function()
            require('colorizer').setup(nil, { css = true })
        end,
    },

    -- Useful plugin to show you pending keybinds.
    {
        'folke/which-key.nvim',
        opts = {},
        lazy = true,
    },

    -- navic complement to breadcumbs
    {
        'utilyre/barbecue.nvim',
        version = '*',
        dependencies = {
            'SmiteshP/nvim-navic',
            'nvim-tree/nvim-web-devicons',
        },
        config = true,
    },

    -- markdown preview :MarkdownPreviewToggle
    {
        'iamcco/markdown-preview.nvim',
        build = function()
            vim.fn['mkdp#util#install']()
        end,
    },

    -- better vim.ui
    {
        'stevearc/dressing.nvim',
        opts = {},
        event = 'VeryLazy',
    },

    -- csv highlight
    {
        'mechatroner/rainbow_csv',
    },
}
