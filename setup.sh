#!/bin/bash -e

source colors.sh

setup_dotfiles(){
    
    # Create bin path ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    new_line
    msg "Create folder to store executables and appImage files"
    print "Create ~/.local/bin folder"
    
    mkdir -p ~/.local/bin
    check_return_code $?
    
    ln -sfv $(pwd)/.local/bin/filter_dir ~/.local/bin
    check_return_code $? ".filter_dir symlink"
    
    # .bash_aliases ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    print "Create symlinks to dotfiles"
    new_line
    
    # Create bash aliases to use aliases
    if [ -f "$HOME/.bash_aliases" ]; then
        msg_update ".bash_aliases"
        rm ~/.bash_aliases
    else
        msg_install ".bash_aliases"
    fi
    
    ln -sfv $(pwd)/.bash_aliases ~/.bash_aliases
    check_return_code $? ".bash_aliases symlink"
    
    # .bashrc ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    # Override .bashrc with my settings
    if [ -f "$HOME/.bashrc" ]; then
        msg_update ".bashrc"
        rm ~/.bashrc
    else
        msg_install ".bashrc"
    fi
    
    ln -sfv $(pwd)/.bashrc ~/.bashrc
    check_return_code $? ".bashrc symlink"
    
    # .gitconfig ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    # Override gitconfig file
    if [ -f "$HOME/.gitconfig" ]; then
        msg_update ".gitconfig"
        rm ~/.gitconfig
    else
        msg_install ".gitconfig"
    fi
    
    ln -sfv $(pwd)/.gitconfig ~/.gitconfig
    check_return_code $? ".gitconfig symlink"
    
}


setup_vscode(){
    
    # Install VS Code and restore settings
    
    msg "Install VS Code and restore settings"
    new_line
    
    if [ ! -f "/etc/apt/sources.list.d/vscode.list" ]; then
        wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
        check_return_code $? "Add VSCode key"
        sudo apt update
        sudo apt install code
        check_return_code $? "Install VS Code"
    fi
    
    msg_install "VS Code extensions"
    cat $(pwd)/.config/Code/extensions.txt | xargs -n 1 code --install-extension
    check_return_code $? "extensions"
    
    # Restaure vscode settings and keybinds
    ln -sfv $(pwd)/.config/Code/keybindings.json ~/.config/Code/User/keybindings.json
    check_return_code $? "keybindings.json symlink"
    
    ln -sfv $(pwd)/.config/Code/settings.json ~/.config/Code/User/settings.json
    check_return_code $? "settings.json symlink"
    
}


setup_google_chrome(){
    
    # Install Chrome ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
    
    # The $? get result of last command
    check_return_code $? "Google Chrome"
    
}

setup_apps(){
    
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
    )
    
    for app in "${snap_apps[@]}"; do
        msg_install "$app"
        
        # Install app
        sudo snap install $app
        
        # The $? get result of last command
        check_return_code $? $app
        
    done
    
    
}

setup_dev_requiements(){
    
    # Install dependencies ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    print "Installing dependencies"
    new_line
    
    apt_apps=(
        "build-essential"
        "make"
        "cmake"
        "dh-make"
        "make"
        "curl"
        "g++"
        "wget"
        "python3-dev"
        "python3-pip"
        "python3-venv"
        "p7zip"
        "p7zip-full"
        "p7zip-rar"
        "unrar"
        "rar"
        "unace-nonfree"
        "ubuntu-restricted-extras"
    )
    
    for app in "${apt_apps[@]}"; do
        msg_install "$app"
        
        # Install app
        sudo apt install $app -y
        
        # The $? get result of last command
        check_return_code $? $app
        
    done
    
}

setup_hosts(){

    msg "Setting /etc/hosts file"

    if [ ! -f "/etc/hosts.bkp" ]; then
        print "Create backup of original file"
        sudo cp /etc/hosts /etc/hosts.bkp
        check_return_code $? "/etc/hosts backup"
    fi

    print "Coping hosts file"
    sudo cp -f $(pwd)/etc/hosts /etc/hosts
    check_return_code $?
    
}

setup_all(){

    setup_dotfiles
    setup_vscode
    setup_google_chrome
    setup_apps
    setup_dev_requiements
    setup_hosts

    print "Update Operational System"
    new_line

    msg_update "apt update"
    sudo apt update
    check_return_code $? "apt update"

    msg_update "apt upgrade"
    sudo apt upgrade -y
    check_return_code $? "apt upgrade"

    msg_update "apt autoremove"
    sudo apt autoremove -y
    check_return_code $? "apt autoremove"

    msg "Install done: `date +%d-%m-%y_%H:%M:%S`"

    new_line

}

usage() {
    echo "Usage:" >&2
    echo "$0 [--dotfiles] [--vscode] [--chrome] [--apps] [--dev] [--hosts]" >&2
    echo "" >&2
    echo "Options:" >&2
    echo "   --dotfiles    Symlink dotfiles in home/ directory" >&2
    echo "   --vscode      Install VsCode and symlink config" >&2
    echo "   --gchrome     Install Google Chrome" >&2
    echo "   --hosts       Create local hosts files and symlink it" >&2
    echo "   --apps        Install development and general applications" >&2
    echo "   --dev         Install development libs" >&2
}


if [ $# -eq 0 ]; then
    usage;
    exit 100;
fi;

for i in "$@"
do
    case $i in
        -d|--dotfiles)
            setup_dotfiles;
        ;;
        --vscode)
            setup_vscode;
        ;;
        --chrome)
            setup_google_chrome;
        ;;
        --apps)
            setup_apps;
        ;;
        --dev)
            setup_dev_requiements
        ;;
        -h|--hosts)
            setup_hosts
        ;;
        -a|--all)
            setup_all
        ;;
        *)
            usage;
            exit 100;
        ;;
    esac
done
