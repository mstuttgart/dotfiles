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

# set -gx TERM xterm-256color
set -gx TERM xterm-kitty
set -gx EDITOR nvim

# add paths to PATH var
set -e fish_user_paths
set -U fish_user_paths $HOME/.local/bin

# ----------------------------------------
# aliases

# exa aliases
alias ls 'eza --color=auto --icons'
alias la 'eza -la --color=auto --icons'
alias ll 'eza -alh --color=auto --icons'
alias lt 'eza -a --tree --color=auto --icons' # show tree in directory

# colorize grep output (good for log files)
alias grep 'grep --color=auto'

# ps aux
abbr pgrep 'ps aux | grep'

# system aliases
abbr aptu 'sudo apt update; sudo apt upgrade -y'
abbr aptr 'sudo apt remove -y'
abbr apti 'sudo apt install'
abbr apts 'apt-cache search'

# create directory recursive
abbr mkdir 'mkdir -pv'

# pyenv aliases
abbr aenv 'source .venv/bin/activate.fish'
abbr cenv 'python -m venv .venv'
abbr denv deactivate

# allows kitty to work with ssh
alias ssh='env TERM=xterm-256color ssh' 

# python server to server files
abbr pyserver 'python3 -m http.server 8000'

# update pip
abbr pipu 'pip install pip --upgrade'
abbr pipr 'pip install -r requirements.txt'

# start starship
starship init fish | source
set -gx STARSHIP_CONFIG $HOME/.config/starship/starship.toml

# add asdf support
source ~/.asdf/asdf.fish

fish_add_path /home/michell/.spicetify
