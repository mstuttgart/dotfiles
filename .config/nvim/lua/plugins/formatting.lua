local plugin = {
  "stevearc/conform.nvim",
  event = { "BufReadPre", "BufNewFile" },
  init = function()
    vim.keymap.set({ "n", "v" }, "<leader>cf", function()
      require("conform").format {
        lsp_fallback = true,
        async = false,
        timeout_ms = 1000,
      }
    end, { desc = "Format file or range (in visual mode)" })
  end,
  config = function()
    require("conform").setup {
      formatters_by_ft = {
        bash = { "shfmt" },
        css = { "prettier" },
        html = { "prettier" },
        javascript = { "prettier" },
        json = { "prettier" },
        lua = { "stylua" },
        markdown = { "markdownlint" },
        python = { "isort", "black" },
        typescript = { "prettier" },
        typescriptreact = { "prettier" },
        xml = { "xmlformat" },
        yaml = { "prettier" },
      },
    }

    require("conform").formatters.xmlformat = {
      prepend_args = { "--blanks", "--indent", "4", "--selfclose" },
    }
  end,
}

return plugin
