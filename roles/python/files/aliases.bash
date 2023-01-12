# Active virtualenv
alias aenv="source .venv/bin/activate"

# Create virtuaenv
alias cenv="python3 -m venv .venv"

# Deactivate virtualenv
alias denv="deactivate"

# Python server to server files
alias pyserver="python3 -m http.server 8000"

# Codigo te ativação do virtualenv emprestado de https://github.com/dhelbegor/oh-my-bashrc/blob/master/bashrc
# env auto activate
function env_auto_activate(){
    if [ -e ".venv" ]; then
        if [ "$VIRTUAL_ENV" != "$(pwd -P)/.venv" ]; then
            _VENV_NAME=$(basename `pwd`)
            echo activating virtualenv \"$_VENV_NAME\"...
            source .venv/bin/activate
            sleep 1
            clear
        fi
    fi
}

export PROMPT_COMMAND=env_auto_activate