# Aliases
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias -- -="cd -"

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
alias ghotfix="git checkout master && git down && git checkout develop && git rebase master && git down && git up"

# System
alias update="sudo apt update && sudo apt upgrade -y"
alias apt-get="sudo apt-get"

# Return my public IP 
alias myip="host myip.opendns.com resolver1.opendns.com | grep \"myip.opendns.com has\" | awk '{print $4}'"

# Python aliases
alias venv="source .venv/bin/activate"
alias cenv="virtualenv -p python3 .venv"
alias denv="deactivate"

# Create vscode extension list
alias vscode-extension-list="code --list-extensions"
