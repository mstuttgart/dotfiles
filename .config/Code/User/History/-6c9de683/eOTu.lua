-- import modules
require("config.options")
require("config.keymaps")
require("config.autocommands")
-- require("config.lazy")

local lazypath = vim.fn.stdpath "data" .. "/lazy/lazy.nvim"

-- bootstrap lazy.nvim!
if not vim.loop.fs_stat(lazypath) then
  require("config.lazy").lazy(lazypath)
end
