-- gitsigns settings
local status, forest = pcall(require, 'everforest')

if (not status) then return end

forest.setup({
  -- 2 will have more UI components be transparent (e.g. status line
  -- background).
  transparent_background_level = 1,
  -- Whether italics should be used for keywords, builtin types and more.
  italics = true,
  -- Disable italic fonts for comments. Comments are in italics by default, set
  -- this to `true` to make them _not_ italic!
  disable_italic_comments = false,
})

-- enable theme
forest.load()
