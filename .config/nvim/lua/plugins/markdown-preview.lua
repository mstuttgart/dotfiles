local plugin = {
  "iamcco/markdown-preview.nvim",
  lazy = true,
  cmd = {
    "MarkdownPreviewToggle",
    "MarkdownPreview",
    "MarkdownPreviewStop",
  },
  ft = { "markdown" },
  build = function()
    vim.fn["mkdp#util#install"]()
  end,
}

return plugin
