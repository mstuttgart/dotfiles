---@type NvPluginSpec[]
local plugins = {

    -- configure syntax highlight
    {
        "nvim-treesitter/nvim-treesitter",
        opts = {
          ensure_installed = {
            -- defaults 
            "vim",
            "lua",
    
            -- web dev 
            "html",
            "css",
            "javascript",
            "typescript",
            "tsx",
            "json",
            -- "vue", "svelte",
    
           -- low level
            "c",
            "zig"
          },
        },
      },
}

return plugins