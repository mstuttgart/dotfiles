# Environment configuration
# This file should be placed at: roles/system/files/.local/share/environment.sh
# Source this in your shell rc files: source ~/.local/share/environment.sh

# =============================================================================
# LANGUAGE & LOCALE
# =============================================================================

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# =============================================================================
# EDITOR
# =============================================================================

export EDITOR=vim
export VISUAL=vim

# =============================================================================
# PATH CONFIGURATIONS
# =============================================================================

# Add local bin directory
export PATH="$HOME/.local/bin:$PATH"

# Add cargo (Rust) to PATH if it exists
if [ -d "$HOME/.cargo/bin" ]; then
  export PATH="$HOME/.cargo/bin:$PATH"
fi

# Add asdf to PATH if it exists
if [ -d "$HOME/.asdf/bin" ]; then
  export PATH="$HOME/.asdf/bin:$PATH"
fi

# =============================================================================
# TOOL CONFIGURATIONS
# =============================================================================

# ripgrep configuration
export RIPGREP_CONFIG_PATH="$HOME/.config/ripgrep/.ripgreprc"

# fzf configuration
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS='--height 50% --reverse --border'

# bat (cat clone) configuration
export BAT_THEME='Dracula'

# =============================================================================
# DOCKER
# =============================================================================

# Docker environment
export DOCKER_HOST="unix:///run/user/$UID/docker.sock"

# =============================================================================
# PYTHON
# =============================================================================

# Python UTF-8 mode
export PYTHONIOENCODING=utf-8

# pipx configuration
export PIPX_HOME="$HOME/.local/pipx"
export PIPX_BIN_DIR="$HOME/.local/bin"

# =============================================================================
# NODE/NVM Configuration (if using asdf)
# =============================================================================

# NodeJS via asdf
export NODE_PATH="$HOME/.asdf/installs/nodejs"
