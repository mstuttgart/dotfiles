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

alias vim 'nvim'

# exa aliases
alias ls 'exa --color=auto'
alias la 'exa -a --color=auto'
alias ll 'exa -alF --color=auto'
alias tree 'exa -a --tree --color=auto' # show tree in directory

# colorize grep output (good for log files)
alias grep 'grep --color=auto'

# confirm before remove
alias rm 'rm -i'

# ps aux alias
alias psgrep 'ps aux | grep'

# system aliases
alias aptu 'sudo apt update && sudo apt upgrade -y'
alias aptr 'sudo apt remove -y'
alias apti 'sudo apt install'
alias apts 'apt-cache search'

# create directory recursive
alias mkdir 'mkdir -pv'

# bat alias
alias cat 'batcat --theme=ansi'

# pyenv aliases
alias aenv 'pyenv activate'
alias cenv 'pyenv virtualenv'
alias denv 'pyenv deactivate'

# python server to server files
alias pyserver 'python3 -m http.server 8000'

# update branchs from hotfix
alias ghotfix 'git stash && git checkout main && git pull --rebase origin main && git checkout develop && git rebase origin/main && git pull --rebase origin develop && git push origin develop'

# alias to manager dotfiles in $HOME
alias dgit  '/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# ----------------------------------------

# configure zoxide
# zoxide init fish | source

# configure pyenv
pyenv init - | source

# start starship
# starship init fish | source
# set -gx STARSHIP_CONFIG $HOME/.config/starship/starship.toml
