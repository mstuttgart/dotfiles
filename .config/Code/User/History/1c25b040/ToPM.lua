local plugin = {
    "mfussenegger/nvim-lint",
    event = {
        "BufReadPre",
        "BufNewFile",
    },
    config = function()
        local lint = require("lint")

        lirequire("lint")nt.linters_by_ft = {
            ansible = { "ansible_lint" },
            bash = { "shellcheck" },
            javascript = { "eslint_d" },
            python = { "pylint" },
            typescript = { "eslint_d" },
        }

        vim.api.nvim_create_autocmd({ "BufWritePost" }, {
            callback = function()
                require("lint").try_lint()
            end,
        })

    end,
}

return plugin
