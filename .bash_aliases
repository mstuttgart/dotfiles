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

# System
alias update="sudo apt update && sudo apt upgrade -y"

# Python aliases
alias venv="source .venv/bin/activate"
alias cenv="virtualenv -p python3 .venv"
alias denv="deactivate"

# Git alias
git remote -v | awk '/fetch/{print $2}' | sed -Ee 's#(git@|git://)#https://#' -e 's@com:@com/@' -e 's%\.git$%%' | awk '/github/'


# Create vscode extension list
alias vscode-extension-list="code --list-extensions"
