# Create bash aliases to use aliases
ln -sfv $(pwd)/.bash_aliases ~/.bash_aliases

# Override .bashrc with my settings
ln -sfv $(pwd)/.bashrc ~/.bashrc

# Override gitconfig file
ln -sfv $(pwd)/.gitconfig ~/.gitconfig
