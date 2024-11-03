#  ~/.zshenv
# Core environment variables

# set XDG directories
export XDG_CONFIG_HOME="${HOME}/.config"
export XDG_DATA_HOME="${HOME}/.local/share"
export XDG_BIN_HOME="${HOME}/.local/bin"
export XDG_LIB_HOME="${HOME}/.local/lib"
export XDG_CACHE_HOME="${HOME}/.cache"

# set default applications
export EDITOR="nvim"
export TERMINAL="alacritty"
export BROWSER="firefox"

# export TERM="xterm-kitty"
#export TERM="alacritty"
# export TERM="xterm-256color"
# export TERM="wezterm"

# others applications
export GIT_CONFIG="${XDG_CONFIG_HOME}/git/.gitconfig"
export PASSWORD_STORE_DIR="${XDG_DATA_HOME}/pass"

# Append Cargo to path, if it's installed
#if [[ -d "$HOME/.cargo/bin" ]]; then
#  export PATH="$HOME/.cargo/bin:$PATH"

  # Add cargo env
#  . "$HOME/.cargo/env"
#fi

# Append .local/bin to path
export PATH="$XDG_BIN_HOME:$PATH"

