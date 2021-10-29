# Aliases
alias ..="cd .."

# Shortcuts
alias work="cd ~/Workspace"
alias dl="cd ~/Downloads"

# Odoo alises
alias odoop="cd ~/Workspace/odoo"
alias odood="cd ~/Workspace/multierp-deploy-scripts"

# Hexo alises
alias hexos="hexo server"
alias hexod="hexo clean && hexo deploy"

# Update branchs from hotfix
alias ghotfix="git checkout main && git down && git checkout develop && git rebase main && git down && git up"

# System
alias update="sudo apt update && sudo apt upgrade -y"

# Return my public IP 
alias myip="host myip.opendns.com resolver1.opendns.com | grep \"myip.opendns.com has\" | awk '{print $4}'"

# Python aliases
alias venv="source .venv/bin/activate"
alias cenv="virtualenv -p python3 .venv"
alias denv="deactivate"
alias pyserver="python3 -m http.server 8000"

# Create vscode extension list
alias vscode-extension-list="code --list-extensions"

# Alias to new apps
alias ls='exa'
alias cat='bat'


