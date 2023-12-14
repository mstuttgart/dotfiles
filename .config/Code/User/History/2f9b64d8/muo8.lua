-- configure formmating

local plugin = {
    "stevearc/conform.nvim",
    dependencies = {
        "WhoIsSethDaniel/mason-tool-installer.nvim",
    },
    event = { "BufReadPre", "BufNewFile" },
    lazy = true,
    keys = {
        {
            "<leader>cf",
            function()
                require("conform").format({ async = true, lsp_fallback = true })
            end,
            mode = "",
            desc = "Format buffer",
        },
    },
    config = function()
        local mason = require("mason")
    
        local mason_tool_installer = require("mason-tool-installer")
    
        -- enable mason and configure icons
        mason.setup({
          ui = {
            icons = {
              package_installed = "✓",
              package_pending = "➜",
              package_uninstalled = "✗",
            },
          },
        })
    
        mason_tool_installer.setup({
          ensure_installed = {
            bash = { "shfmt" },
            css = { "prettier" },
            html = { "prettier" },
            javascript = { "prettier" },
            json = { "prettier" },
            lua = { "stylua" },
            markdown = { "prettier" },
            python = { "isort", "autopep8" },
            typescript = { "prettier" },
            xml = { "xmlformat" },
            yaml = { "prettier" },
          },
        })
    end,
      
    opts = {
        -- Define formatters
        formatters_by_ft = {
            bash = { "shfmt" },
            css = { "prettier" },
            html = { "prettier" },
            javascript = { "prettier" },
            json = { "prettier" },
            lua = { "stylua" },
            markdown = { "prettier" },
            python = { "isort", "autopep8" },
            typescript = { "prettier" },
            xml = { "xmlformat" },
            yaml = { "prettier" },
        },

    },
}

return plugin
