# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH
export TERM="xterm-kitty"

# configure zsh history
HISTFILE=$HOME/.histfile
HISTSIZE=1000
SAVEHIST=1000

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='nvim'
fi

# ----------------------------------------
# Install zplug and zsh plugins
# zplug 
[[ ! -f ~/.zplug/init.zsh ]] || source ~/.zplug/init.zsh

# Install zplug
zplug "zplug/zplug", hook-build:"zplug --self-manage"

# plguins from oh-my-zsh
zplug "plugins/git", from:oh-my-zsh
zplug "plugins/asdf", from:oh-my-zsh
zplug "plugins/fzf", from:oh-my-zsh
zplug "plugins/virtualenvwrapper", from:oh-my-zsh

# install others plugs 
zplug "zsh-users/zsh-syntax-highlighting"
zplug "zsh-users/zsh-autosuggestions"
zplug "agkozak/zsh-z"
zplug "hlissner/zsh-autopair"

# Load theme file
# zplug "spaceship-prompt/spaceship-prompt", use:spaceship.zsh, from:github, as:theme

# Install plugins if there are plugins that have not been installed
if ! zplug check; then
    zplug install
fi

# Then, source plugins and add commands to $PATH
zplug load

# spaceship theme configuration
SPACESHIP_PROMPT_ORDER=(
  venv          # virtualenv section
  user          # Username section
  dir           # Current directory section
  host          # Hostname section
  git           # Git section (git_branch + git_status)
  exec_time     # Execution time
  line_sep      # Line break
  jobs          # Background jobs indicator
  exit_code     # Exit code section
  char          # Prompt character
)

SPACESHIP_USER_SHOW=always
SPACESHIP_PROMPT_ADD_NEWLINE=false
SPACESHIP_CHAR_SYMBOL="❯"
SPACESHIP_CHAR_SUFFIX=" "

# ----------------------------------------
# aliases
#
alias cp="cp -iv"
alias mkdir="mkdir -pv"
alias mv="mv -iv"

alias rm="rm -rf --"

# eza aliases
alias ls="exa --color=auto --icons"
alias la="exa -la --color=auto --icons"
alias ll="exa -alh --color=auto --icons"
alias lt="exa -a --tree --color=auto --icons" # show tree in directory

# colorize grep output (good for log files)
alias grep="grep --color=auto"

# ps aux
alias pgrep="ps aux | grep"

# system aliases
alias aptu="sudo apt update; sudo apt upgrade -y"
alias aptr="sudo apt remove"
alias apti="sudo apt install"
alias apts="apt-cache search"

# clear terminal
alias cls="clear"

# create directory recursive
alias mkdir="mkdir -pv"

# pyenv aliases
alias aenv="source .venv/bin/activate"
alias cenv="python3 -m venv .venv"
alias denv="deactivate"

# using terminfo of kitty in ssh
alias ssh="TERM=xterm-256color ssh"

# python server to server files
alias pyserver="python3 -m http.server 8000"

# update pip
alias pipu="pip install pip --upgrade"
alias pipr="pip install -r requirements.txt"

export PATH=$PATH:/home/michell/.spicetify

# configure starship prompt theme
export STARSHIP_CONFIG="$HOME/.config/starship/starship.toml"
eval "$(starship init zsh)"
