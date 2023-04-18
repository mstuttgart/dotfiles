# Aliases
alias ..="cd .."

# Shortcuts
alias dwork="cd ~/Workspace"
alias ddown="cd ~/Downloads"
alias ddot="cd ~/.dotfiles"

# System
alias update="sudo apt update && sudo apt upgrade -y"
alias autoremove="sudo apt autoremove -y"
alias apti="sudo apt install"
alias apts="apt-cache search"

# Return my public IP
alias myip="host myip.opendns.com resolver1.opendns.com | grep \"myip.opendns.com has\" | awk '{print $4}'"

# Return net devices
alias netdevice="ip link"

# Call gogh to change console theme
alias gogh='bash -c "$(wget -qO- https://git.io/vQgMr)"'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# List process
alias psgrep="ps aux | grep"
alias kill9="sudo kill -9"

# Create directory recursive
alias mkdir="mkdir -pv"

# exa alias
alias ls="exa --color=auto"
alias ll='exa -alF'
alias la='exa -a'
alias ldir='exa -lD1'
alias tree='exa --tree'

# bat alias
alias cat="batcat --theme=ansi"

# nvim alias
alias vim="nvim"

# Python aliases
# Active virtualenv
alias aenv="source .venv/bin/activate"

# Create virtuaenv
alias cenv="python3 -m venv .venv"

# Deactivate virtualenv
alias denv="deactivate"

# Install requirements
alias pipreq="pip install -r requirements.txt"

# Python server to server files
alias pyserver="python3 -m http.server 8000"

alias config='/usr/bin/git --git-dir=/home/michell/.cfg/.git/ --work-tree=/home/michell'
