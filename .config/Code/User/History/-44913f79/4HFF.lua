---@type ChadrcConfig
local M = {}

M.plugins = "custom.plugins"
M.mappings = require "custom.mappings"

M.ui = {
    theme = 'everforest',
    statusline = {
        theme = "vscode_colored", -- default/vscode/vscode_colored/minimal
    },
}

return M
