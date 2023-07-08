-- lsp settings
--
-- NOTE: This is where your plugins related to LSP can be installed.
--  The configuration is done below. Search for lspconfig to find it below.
--
-- local plugin2 = {
--     -- LSP Configuration & Plugins
--     'neovim/nvim-lspconfig',
--     dependencies = {
--         -- Automatically install LSPs to stdpath for neovim
--         { 'williamboman/mason.nvim', config = true, build = ':MasonUpdate' },
--         'williamboman/mason-lspconfig.nvim',
--
--         -- Useful status updates for LSP
--         -- NOTE: `opts = {}` is the same as calling `require('fidget').setup({})`
--         { 'j-hui/fidget.nvim', opts = {} },
--
--         -- Additional lua configuration, makes nvim stuff amazing!
--         'folke/neodev.nvim',
--     },
--     cmd = { 'Mason', 'LspInstall', 'LspUnInstall' },
--     init = function()
--         -- Diagnostic keymaps
--         vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, { desc = 'Go to previous diagnostic message' })
--         vim.keymap.set('n', ']d', vim.diagnostic.goto_next, { desc = 'Go to next diagnostic message' })
--         vim.keymap.set('n', '<leader>e', vim.diagnostic.open_float, { desc = 'Open floating diagnostic message' })
--         vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, { desc = 'Open diagnostics list' })
--
--         -- LSP settings.
--         --  This function gets run when an LSP connects to a particular buffer.
--         local on_attach = function(_, bufnr)
--             -- NOTE: Remember that lua is a real programming language, and as such it is possible
--             -- to define small helper and utility functions so you don't have to repeat yourself
--             -- many times.
--             --
--             -- In this case, we create a function that lets us more easily define mappings specific
--             -- for LSP related items. It sets the mode, buffer and description for us each time.
--             local nmap = function(keys, func, desc)
--                 if desc then
--                     desc = 'LSP: ' .. desc
--                 end
--
--                 vim.keymap.set('n', keys, func, { buffer = bufnr, desc = desc })
--             end
--
--             nmap('<leader>rn', vim.lsp.buf.rename, '[R]e[n]ame')
--             -- nmap('<leader>ca', vim.lsp.buf.code_action, '[C]ode [A]ction')
--
--             nmap('gd', vim.lsp.buf.definition, '[G]oto [D]efinition')
--             nmap('gr', require('telescope.builtin').lsp_references, '[G]oto [R]eferences')
--             nmap('gI', vim.lsp.buf.implementation, '[G]oto [I]mplementation')
--             -- nmap('<leader>D', vim.lsp.buf.type_definition, 'Type [D]efinition')
--             nmap('<leader>ds', require('telescope.builtin').lsp_document_symbols, '[D]ocument [S]ymbols')
--             nmap('<leader>ws', require('telescope.builtin').lsp_dynamic_workspace_symbols, '[W]orkspace [S]ymbols')
--
--             -- See `:help K` for why this keymap
--             nmap('K', vim.lsp.buf.hover, 'Hover Documentation')
--             nmap('<C-k>', vim.lsp.buf.signature_help, 'Signature Documentation')
--
--             -- Lesser used LSP functionality
--             nmap('gD', vim.lsp.buf.declaration, '[G]oto [D]eclaration')
--             nmap('<leader>wa', vim.lsp.buf.add_workspace_folder, '[W]orkspace [A]dd Folder')
--             nmap('<leader>wr', vim.lsp.buf.remove_workspace_folder, '[W]orkspace [R]emove Folder')
--             nmap('<leader>wl', function()
--                 print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
--             end, '[W]orkspace [L]ist Folders')
--
--             vim.api.nvim_create_autocmd('BufWritePre', {
--                 buffer = bufnr,
--                 callback = function()
--                     vim.lsp.buf.format { async = false }
--                 end,
--             })
--
--             require('nvim-navic').attach(client, bufnr)
--         end
--
--         -- Enable the following language servers
--         local servers = {
--             pyright = {},
--             yamlls = {},
--             html = {},
--             cssls = {},
--             lemminx = {},
--             lua_ls = {
--                 Lua = {
--                     workspace = { checkThirdParty = false },
--                     telemetry = { enable = false },
--                 },
--             },
--         }
--
--         -- Setup neovim lua configuration
--         require('neodev').setup()
--
--         -- nvim-cmp supports additional completion capabilities, so broadcast that to servers
--         local capabilities = vim.lsp.protocol.make_client_capabilities()
--         capabilities = require('cmp_nvim_lsp').default_capabilities(capabilities)
--
--         -- Ensure the servers above are installed
--         local mason_lspconfig = require('mason-lspconfig')
--
--         mason_lspconfig.setup {
--             ensure_installed = vim.tbl_keys(servers),
--         }
--
--         mason_lspconfig.setup_handlers {
--             function(server_name)
--                 require('lspconfig')[server_name].setup {
--                     capabilities = capabilities,
--                     on_attach = on_attach,
--                     flags = { debounce_text_changes = 300 },
--                     settings = servers[server_name],
--                 }
--             end,
--         }
--
--         vim.lsp.handlers['textDocument/publishDiagnostics'] = vim.lsp.with(vim.lsp.diagnostic.on_publish_diagnostics, {
--             -- Disable underline, it's very annoying
--             underline = false,
--             virtual_text = false,
--             -- Enable virtual text, override spacing to 4
--             -- virtual_text = {spacing = 4},
--             -- Use a function to dynamically turn signs off
--             -- and on, using buffer local variables
--             signs = true,
--             update_in_insert = false,
--         })
--     end,
-- }
--
local plugin = {
    {
        'VonHeikemen/lsp-zero.nvim',
        branch = 'v2.x',
        dependencies = {
            -- LSP Support
            { 'neovim/nvim-lspconfig' }, -- Required
            { -- Optional
                'williamboman/mason.nvim',
                build = function()
                    pcall(vim.cmd, 'MasonUpdate')
                end,
            },
            { 'williamboman/mason-lspconfig.nvim' }, -- Optional
            'folke/neodev.nvim',

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

            -- complements
            'onsails/lspkind-nvim', -- add the nice source + completion item kind to the menu
        },
        init = function()
            require('mason').setup {
                ui = {
                    border = 'rounded',
                },
            }
            local lsp = require('lsp-zero').preset {}

            lsp.on_attach(function(client, bufnr)
                lsp.default_keymaps { buffer = bufnr }
                lsp.buffer_autoformat()
            end)

            lsp.set_sign_icons {
                error = '✘',
                warn = '▲',
                hint = '⚑',
                info = '»',
            }

            lsp.ensure_installed {
                -- Replace these with whatever servers you want to install
                'pyright',
                'yamlls',
                'html',
                'cssls',
                'lemminx',
            }

            -- (Optional) Configure lua language server for neovim
            require('lspconfig').lua_ls.setup(lsp.nvim_lua_ls())

            lsp.setup()
        end,
    },
}

return plugin
