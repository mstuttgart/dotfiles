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
        local conform = require("conform")
    
        conform.setup({
          formatters_by_ft = {
            javascript = { "prettier" },
            typescript = { "prettier" },
            javascriptreact = { "prettier" },
            typescriptreact = { "prettier" },
            svelte = { "prettier" },
            css = { "prettier" },
            html = { "prettier" },
            json = { "prettier" },
            yaml = { "prettier" },
            markdown = { "prettier" },
            graphql = { "prettier" },
            lua = { "stylua" },
            python = { "isort", "black" },
          },
        })
    
        vim.keymap.set({ "n", "v" }, "<leader>mp", function()
          conform.format({
            lsp_fallback = true,
            async = false,
            timeout_ms = 500,
          })
        end, { desc = "Format file or range (in visual mode)" })
    end,
      
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
