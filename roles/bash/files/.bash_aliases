# Aliases
alias ..="cd .."

# Shortcuts
alias work="cd ~/Workspace"
alias dl="cd ~/Downloads"

# System
alias update="sudo apt update && sudo apt upgrade -y"
alias autoremove="sudo apt autoremove -y"

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
