-- import modules
require("config.options")
require("config.keymaps")
require("config.autocommands")
require("config.lazy")

-- pcall(vim.cmd.colorscheme, 'everforest')
-- pcall(vim.cmd.colorscheme, 'tokyonight')
vim.cmd[[ colorscheme everforest ]]
