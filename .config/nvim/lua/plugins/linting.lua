local plugin = {
  "mfussenegger/nvim-lint",
  event = { "BufReadPre", "BufNewFile" },
  init = function()
    vim.keymap.set("n", "<leader>cl", function()
      require("lint").try_lint()
    end, { desc = "Trigger linting for current file" })
  end,
  config = function()
    local lint = require "lint"

    lint.linters_by_ft = {
      ansible = { "ansible_lint" },
      bash = { "shellcheck" },
      javascript = { "eslint_d" },
      javascriptreact = { "eslint_d" },
      markdown = { "markdownlint" },
      python = { "pylint" },
      typescript = { "eslint_d" },
      typescriptreact = { "eslint_d" },
      yaml = { "yamllint" },
    }

    local lint_augroup = vim.api.nvim_create_augroup("lint", { clear = true })

    vim.api.nvim_create_autocmd({ "BufEnter", "BufWritePost", "InsertLeave" }, {
      group = lint_augroup,
      callback = function()
        lint.try_lint()
      end,
    })
  end,
}

return plugin
