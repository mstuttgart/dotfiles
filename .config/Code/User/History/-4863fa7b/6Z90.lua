-- configure bufferline

require("bufferline").setup {
  options = {
    themable = true,
    close_command = function(n)
      require("mini.bufremove").delete(n, false)
    end,
    right_mouse_command = function(n)
      require("mini.bufremove").delete(n, false)
    end,
    diagnostics = "nvim_lsp",
    separator_style = "thin",
    always_show_bufferline = true,
    offsets = {
      {
        filetype = "NvimTree",
        text = "",
        highlight = "Directory",
        text_align = "left",
        separator = false,
      },
    },
  },
}
