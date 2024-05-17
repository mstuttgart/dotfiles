# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH
# export TERM="xterm-kitty"
# export TERM="alacritty"
# export TERM="xterm-256color"
export TERM="wezterm"

# configure zsh history
HISTFILE=$HOME/.histfile
HISTSIZE=1000
SAVEHIST=1000

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'

  # fix ctrl+p, ctrl+n, ctrl+f and etc not work on tmux and others terminals
  # https://superuser.com/questions/750965/tmux-printing-p
  bindkey -e
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

# Install plugins if there are plugins that have not been installed
if ! zplug check; then
    zplug install
fi

# Then, source plugins and add commands to $PATH
zplug load

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

# nvim aliases
alias nvimconf="cd $HOME/.config/nvim && nvim"
alias nvimclean="nvim --clean"
alias nvimdel="rm -rf $HOME/.local/share/nvim $HOME/.cache/nvim"

# i3 aliases 
alias i3conf="nvim $HOME/.config/i3/config"

# wezterm aliases
alias wezconf="nvim $HOME/.config/wezterm/wezterm.lua"

# spicetify part (theme spotify)
export PATH=$PATH:/home/michell/.spicetify

# configure starship prompt theme
export STARSHIP_CONFIG="$HOME/.config/starship/starship.toml"
eval "$(starship init zsh)"
