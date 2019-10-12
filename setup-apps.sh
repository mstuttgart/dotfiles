
source colors.sh

# Install apt apps ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

new_line
print "Installing apt Apps"
new_line

apt_apps=(
    "gpick"
    "htop"
    "tree"
    "screenfetch"
    "tig"
    "git"
    "git-core"
    "cmus"
    "flameshot"
    "sqlitebrowser"
    "snapd"
)

for app in "${apt_apps[@]}"; do
    msg_install "$app"
    
    # Install app
    sudo apt install $app -y
    
    # The $? get result of last command
    check_return_code $? $app
    
done

# Install snap apps ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

msg "Installing Snap packages"
new_line

snap_apps=(
    "core"
    "code --classic"
    "chromium"
    "spotify"
    "postman"
)

for app in "${snap_apps[@]}"; do
    msg_install "$app"
    
    # Install app
    sudo snap install $app
    
    # The $? get result of last command
    check_return_code $? $app
    
done

# Restaure VS Code settings ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

msg "Restaure VS Code Settings"
new_line

msg_install "VS Code extensions"
cat vscode/extensions.txt | xargs -n 1 code --install-extension
check_return_code $? "extensions"

# Restaure vscode settings and keybinds
ln -sfv $(pwd)/vscode/keybindings.json ~/.config/Code/User/keybindings.json
check_return_code $? "keybindings.json symlink"

ln -sfv $(pwd)/vscode/settings.json ~/.config/Code/User/settings.json
check_return_code $? "settings.json symlink"

msg_ok "Installing Apps done"
