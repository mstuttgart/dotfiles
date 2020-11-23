
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
    "pgadmin3"
    "snapd"
    "software-properties-common"
    "gdebi"
    "vlc"
    "libreoffice"
    "gparted"
    "fonts-firacode"
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
    "postman"
    "spotify"
    "onefetch"
)

for app in "${snap_apps[@]}"; do
    msg_install "$app"
    
    # Install app
    sudo snap install $app
    
    # The $? get result of last command
    check_return_code $? $app
    
done

# Install Chrome ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# The $? get result of last command
check_return_code $? "Google Chrome"

# Install VS Code and restore settings ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

msg "Install VS Code and restore settings"
new_line

wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
check_return_code $? "Add VSCode key"

sudo apt update
sudo apt install code
check_return_code $? "Install VS Code"

msg_install "VS Code extensions"
cat vscode/extensions.txt | xargs -n 1 code --install-extension
check_return_code $? "extensions"

# Restaure vscode settings and keybinds
ln -sfv $(pwd)/vscode/keybindings.json ~/.config/Code/User/keybindings.json
check_return_code $? "keybindings.json symlink"

ln -sfv $(pwd)/vscode/settings.json ~/.config/Code/User/settings.json
check_return_code $? "settings.json symlink"

# Install vscode dev fonts
sudo apt install fonts-firacode -y

msg_ok "Installing Apps done"
