# Custom shell functions and utilities
# This file should be placed at: roles/shell/files/.local/share/zsh/functions.zsh

# Directory navigation with fuzzy finder
fzf-cd() {
  local dir=$(find ${1:-.} -type d -name .git -prune -o -type d -print 2>/dev/null | fzf --preview 'ls -la {}' --preview-window right:30%)
  if [ -n "$dir" ]; then
    cd "$dir"
  fi
}

# Git branch selector
fzf-git-branch() {
  local branch=$(git branch --all | grep -v HEAD | sed 's/.* //' | fzf --preview 'git log -1 --oneline {}')
  if [ -n "$branch" ]; then
    git checkout "$branch"
  fi
}

# Search in file history
fzf-history() {
  eval $( ([ -n "$ZSH_NAME" ] && fc -l 1 || history) | fzf +s --tac | sed 's/ *[0-9]* *//')
}

# Find and open file with editor
fzf-edit() {
  local file=$(find ${1:-.} -type f -name .git -prune -o -type f -print 2>/dev/null | fzf --preview 'head -20 {}' --preview-window right:40%)
  if [ -n "$file" ]; then
    $EDITOR "$file"
  fi
}

# Quick grep with fzf
fzf-grep() {
  local pattern=$1
  if [ -z "$pattern" ]; then
    echo "Usage: fzf-grep <pattern>"
    return 1
  fi
  rg "$pattern" --files-with-matches | fzf --preview "rg --color always '$pattern' {}"
}

# List and kill processes
fzf-kill() {
  ps aux | fzf --header "Select process to kill" | awk '{print $2}' | xargs kill -9
}
