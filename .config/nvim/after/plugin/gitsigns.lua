-- gitsigns settings
local status, gitsigns = pcall(require, 'gitsigns')

if (not status) then return end

gitsigns.setup {
  current_line_blame = true,
  current_line_blame_formatter_opts = {
    relative_time = false,
  },
}
