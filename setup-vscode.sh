# Restaure vscode settings and keybinds
ln -sfv $(pwd)/vscode/keybindings.json ~/.config/Code/User/keybindings.json
ln -sfv $(pwd)/vscode/settings.json ~/.config/Code/User/settings.json

cat vscode/extensions.txt | xargs -n 1 code --install-extension
