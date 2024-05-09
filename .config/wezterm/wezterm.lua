-- Pull in the wezterm API
local wezterm = require("wezterm")

-- local act = wezterm.action

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme_dirs = { "$HOME/.config/wezterm/themes" }
config.color_scheme = "Everforest Dark (Medium)"

config.font = wezterm.font("JetBrainsMono Nerd Font")
config.font_size = 12.0

-- Dim inactive panes
config.inactive_pane_hsb = {
	-- NOTE: these values are multipliers, applied on normal pane values
	saturation = 1,
	brightness = 0.9,
}

	-- Tab Bar
config.enable_tab_bar = false
config.hide_tab_bar_if_only_one_tab = true
config.adjust_window_size_when_changing_font_size = false

config.use_dead_keys = false
config.scrollback_lines = 5000

config.window_padding = {
	left = 3,
	right = 3,
	top = 3,
	bottom = 3,
}

	-- Aesthetic Night Colorscheme
config.bold_brightens_ansi_colors = true



config.window_frame = {
	font = wezterm.font({ family = "Noto Sans", weight = "Regular" }),
}

config.disable_default_key_bindings = true
config.leader = { key = "b", mods = "CMD", timeout_milliseconds = 2000 }
config.automatically_reload_config = true

-- Keybinds

config.disable_default_key_bindings = true
config.keys = {
	{
		key = [[\]],
		mods = "CTRL|ALT",
		action = wezterm.action({
			SplitHorizontal = { domain = "CurrentPaneDomain" },
		}),
	},
	{
		key = [[\]],
		mods = "CTRL",
		action = wezterm.action({
			SplitVertical = { domain = "CurrentPaneDomain" },
		}),
	},
	{
		key = "q",
		mods = "CTRL",
		action = wezterm.action({ CloseCurrentPane = { confirm = false } }),
	},
	{
		key = "h",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ ActivatePaneDirection = "Left" }),
	},
	{
		key = "l",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ ActivatePaneDirection = "Right" }),
	},
	{
		key = "k",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ ActivatePaneDirection = "Up" }),
	},
	{
		key = "j",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ ActivatePaneDirection = "Down" }),
	},
	{
		key = "h",
		mods = "CTRL|SHIFT|ALT",
		action = wezterm.action({ AdjustPaneSize = { "Left", 1 } }),
	},
	{
		key = "l",
		mods = "CTRL|SHIFT|ALT",
		action = wezterm.action({ AdjustPaneSize = { "Right", 1 } }),
	},
	{
		key = "k",
		mods = "CTRL|SHIFT|ALT",
		action = wezterm.action({ AdjustPaneSize = { "Up", 1 } }),
	},
	{
		key = "j",
		mods = "CTRL|SHIFT|ALT",
		action = wezterm.action({ AdjustPaneSize = { "Down", 1 } }),
	},
	{ -- browser-like bindings for tabbing
		key = "t",
		mods = "CTRL",
		action = wezterm.action({ SpawnTab = "CurrentPaneDomain" }),
	},
	{
		key = "q",
		mods = "CTRL",
		action = wezterm.action({ CloseCurrentTab = { confirm = false } }),
	},
	{
		key = "Tab",
		mods = "CTRL",
		action = wezterm.action({ ActivateTabRelative = 1 }),
	},
	{
		key = "Tab",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ ActivateTabRelative = -1 }),
	}, -- standard copy/paste bindings
	{
		key = "x",
		mods = "CTRL",
		action = "ActivateCopyMode",
	},
	{
		key = "v",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ PasteFrom = "Clipboard" }),
	},
	{
		key = "c",
		mods = "CTRL|SHIFT",
		action = wezterm.action({ CopyTo = "ClipboardAndPrimarySelection" }),
	},
}

-- and finally, return the configuration to wezterm
return config
