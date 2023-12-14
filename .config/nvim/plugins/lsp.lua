-- lsp settings
--
local plugin = {
    'VonHeikemen/lsp-zero.nvim',
    branch = 'v2.x',
    dependencies = {
        -- LSP Support
        { 'neovim/nvim-lspconfig' },
        {
            'williamboman/mason.nvim',
            build = function()
                pcall(vim.cmd, 'MasonUpdate')
            end,
        },
        'williamboman/mason-lspconfig.nvim',
        -- Autocompletion
        -- completion sources
        'hrsh7th/cmp-nvim-lsp',
        'hrsh7th/cmp-nvim-lua',
        'hrsh7th/cmp-buffer',
        'hrsh7th/cmp-cmdline',
        'hrsh7th/nvim-cmp',
        'hrsh7th/cmp-path',
        'saadparwaiz1/cmp_luasnip',
        'L3MON4D3/LuaSnip',
        'rafamadriz/friendly-snippets',
        'onsails/lspkind-nvim',
    },
    init = function()
        require('mason').setup({
            ui = {
                icons = {
                    package_installed = "✓",
                    package_pending = "➜",
                    package_uninstalled = "✗",
                },
            },
        })

        require('mason-lspconfig').setup({
            ensure_installed = {
                'pyright',
                'html',
                'cssls',
                'lua_ls',
                'bashls',
                'ansiblels',
            }
        })

        -- require('cmp').setup({
        --     opts = function(_, opts)
        --         local has_words_before = function()
        --             unpack = unpack or table.unpack
        --             local line, col = unpack(vim.api.nvim_win_get_cursor(0))
        --             return col ~= 0 and
        --                 vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
        --         end

        --         local luasnip = require("luasnip")
        --         local cmp = require("cmp")

        --         opts.mapping = vim.tbl_extend("force", opts.mapping, {
        --             ["<Tab>"] = cmp.mapping(function(fallback)
        --                 if cmp.visible() then
        --                     -- You could replace select_next_item() with confirm({ select = true }) to get VS Code autocompletion behavior
        --                     cmp.select_next_item()
        --                     -- You could replace the expand_or_jumpable() calls with expand_or_locally_jumpable()
        --                     -- this way you will only jump inside the snippet region
        --                 elseif luasnip.expand_or_jumpable() then
        --                     luasnip.expand_or_jump()
        --                 elseif has_words_before() then
        --                     cmp.complete()
        --                 else
        --                     fallback()
        --                 end
        --             end, { "i", "s" }),
        --             ["<S-Tab>"] = cmp.mapping(function(fallback)
        --                 if cmp.visible() then
        --                     cmp.select_prev_item()
        --                 elseif luasnip.jumpable(-1) then
        --                     luasnip.jump(-1)
        --                 else
        --                     fallback()
        --                 end
        --             end, { "i", "s" }),
        --         })

        --         mapping = {

        --             ['<C-n>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Insert }),
        --             ['<C-p>'] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Insert }),
        --             ['<Down>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Select }),
        --             ['<Up>'] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Select }),
        --             ['<C-d>'] = cmp.mapping.scroll_docs(-4),
        --             ['<C-f>'] = cmp.mapping.scroll_docs(4),
        --             ['<C-Space>'] = cmp.mapping.complete(),
        --             ['<C-e>'] = cmp.mapping.close(),
        --             ['<CR>'] = cmp.mapping.confirm({
        --                 behavior = cmp.ConfirmBehavior.Replace,
        --                 select = true,
        --             }),

        --             ['<Tab>'] = function(fallback)
        --                 if cmp.visible() then
        --                     cmp.select_next_item()
        --                 elseif luasnip.expand_or_jumpable() then
        --                     vim.fn.feedkeys(vim.api.nvim_replace_termcodes('<Plug>luasnip-expand-or-jump', true, true, true),
        --                         '')
        --                 else
        --                     fallback()
        --                 end
        --             end,
        --             ['<S-Tab>'] = function(fallback)
        --                 if cmp.visible() then
        --                     cmp.select_prev_item()
        --                 elseif luasnip.jumpable(-1) then
        --                     vim.fn.feedkeys(vim.api.nvim_replace_termcodes('<Plug>luasnip-jump-prev', true, true, true), '')
        --                 else
        --                     fallback()
        --                 end
        --             end,

        --         },

        --         snippet = {
        --             expand = function(args)
        --                 require('luasnip').lsp_expand(args.body)
        --             end,
        --         },
        --         sources = {
        --             { name = 'cmp_tabnine' },
        --             { name = 'luasnip' },
        --             { name = 'path' },
        --         },

        --     end,
        --     config = function(_, opts)
        --         require("cmp").setup(opts)
        --     end,
        -- })
        local cmp = require'cmp'

        cmp.setup({
            mapping = {

                ['<C-n>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Insert }),
                ['<C-p>'] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Insert }),
                ['<Down>'] = cmp.mapping.select_next_item({ behavior = cmp.SelectBehavior.Select }),
                ['<Up>'] = cmp.mapping.select_prev_item({ behavior = cmp.SelectBehavior.Select }),
                ['<C-d>'] = cmp.mapping.scroll_docs(-4),
                ['<C-f>'] = cmp.mapping.scroll_docs(4),
                ['<C-Space>'] = cmp.mapping.complete(),
                ['<C-e>'] = cmp.mapping.close(),
                ['<CR>'] = cmp.mapping.confirm({
                    behavior = cmp.ConfirmBehavior.Replace,
                    select = true,
                }),

                ['<Tab>'] = function(fallback)
                    if cmp.visible() then
                        cmp.select_next_item()
                    elseif luasnip.expand_or_jumpable() then
                        vim.fn.feedkeys(vim.api.nvim_replace_termcodes('<Plug>luasnip-expand-or-jump', true, true, true),
                            '')
                    else
                        fallback()
                    end
                end,
                ['<S-Tab>'] = function(fallback)
                    if cmp.visible() then
                        cmp.select_prev_item()
                    elseif luasnip.jumpable(-1) then
                        vim.fn.feedkeys(vim.api.nvim_replace_termcodes('<Plug>luasnip-jump-prev', true, true, true), '')
                    else
                        fallback()
                    end
                end,

            },

            snippet = {
                expand = function(args)
                    require('luasnip').lsp_expand(args.body)
                end,
            },
            sources = {
                { name = 'cmp_tabnine' },
                { name = 'luasnip' },
                { name = 'path' },
            },
        })

        vim.o.completeopt = 'menuone,noselect'

        local lsp = require('lsp-zero').preset {}

        lsp.on_attach(function(client, bufnr)
            lsp.default_keymaps { buffer = bufnr }
            -- lsp.buffer_autoformat()
        end)

        lsp.set_sign_icons {
            error = '✘',
            warn = '▲',
            hint = '⚑',
            info = '»',
        }

        -- (Optional) Configure lua language server for neovim
        require('lspconfig').lua_ls.setup({})
        require('lspconfig').pyright.setup({})
        require('lspconfig').bashls.setup({})



        lsp.setup()

        local capabilities = vim.lsp.protocol.make_client_capabilities()
        capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)

        local lspconfig = require('lspconfig')
        local get_servers = require('mason-lspconfig').get_installed_servers

        for _, server_name in ipairs(get_servers()) do
            lspconfig[server_name].setup({
                capabilities = capabilities,
            })
        end
    end,
}

return plugin
