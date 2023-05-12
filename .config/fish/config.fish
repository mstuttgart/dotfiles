# fish shell settings

# disable initial message of fish
set -U fish_greeting

# ----------------------------------------
# general settings

# themes configs
set -g theme_display_user yes
set -g theme_hide hostname no
set -g theme_hostname always

# ----------------------------------------
# set global (export) values

set -gx TERM xterm-256color
set -gx EDITOR nvim

# add paths to PATH var
set -e fish_user_paths
set -U fish_user_paths $HOME/.local/bin

# pyenv configs
set -Ux PYENV_ROOT $HOME/.pyenv
set -U fish_user_paths $PYENV_ROOT/bin

# ----------------------------------------
# aliases

# exa aliases
abbr ls 'exa --color=auto --icons'
abbr la 'exa -a --color=auto --icons'
abbr ll 'exa -alh --color=auto --icons'
abbr lt 'exa -a --tree --color=auto --icons' # show tree in directory

# bat aliases
abbr cat 'batcat --theme=everforest'

# colorize grep output (good for log files)
abbr grep 'grep --color=auto'

# confirm before remove
abbr rm 'rm -i'

# ps aux
abbr psgrep 'ps aux | grep'

# system aliases
abbr aptu 'sudo apt update; sudo apt upgrade -y'
abbr aptr 'sudo apt remove -y'
abbr apti 'sudo apt install'
abbr apts 'apt-cache search'

# create directory recursive
abbr mkdir 'mkdir -pv'

# pyenv aliases
abbr aenv 'pyenv activate'
abbr cenv 'pyenv virtualenv'
abbr denv 'pyenv deactivate'

# python server to server files
abbr pyserver 'python3 -m http.server 8000'

# configure pyenv
pyenv init - | source

# condigure pyenv-virtualenv
status --is-interactive; and pyenv virtualenv-init - | source

# start starship
starship init fish | source
set -gx STARSHIP_CONFIG $HOME/.config/starship/starship.toml

# configure asdf
source ~/.asdf/asdf.fish
