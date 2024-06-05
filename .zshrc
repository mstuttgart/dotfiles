# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# configure zsh history
HISTFILE="${HOME}/.histfile"
HISTSIZE=5000
SAVEHIST=5000

# Preferred editor for local and remote sessions
if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'

  # fix ctrl+p, ctrl+n, ctrl+f and etc not work on tmux and others terminals
  # https://superuser.com/questions/750965/tmux-printing-p
  bindkey -e
fi

# fix ctrl+p, ctrl+n, ctrl+f and etc not work on tmux and others terminals
# https://superuser.com/questions/750965/tmux-printing-p
bindkey -e

# ----------------------------------------
# Install zplug and zsh plugins
# zplug 
[[ ! -f "${HOME}/.zplug/init.zsh" ]] || source "${HOME}/.zplug/init.zsh"

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
zplug "zsh-users/zsh-completions"
zplug "agkozak/zsh-z"
zplug "hlissner/zsh-autopair"

# Install plugins if there are plugins that have not been installed
if ! zplug check; then
  zplug install
fi

# Then, source plugins and add commands to $PATH
zplug load

# load aliases
if [ -f "${HOME}/.zsh_aliases" ]; then
  . "${HOME}/.zsh_aliases"
fi

# spicetify part (theme spotify)
export PATH=$PATH:/home/michell/.spicetify

# configure starship prompt theme
export STARSHIP_CONFIG="${XDG_CONFIG_HOME}/starship/starship.toml"
eval "$(starship init zsh)"

