#!/bin/bash -e

source colors.sh

setup_dotfiles(){
    
    # Create bin path ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    new_line
    msg "Create folder to store executables and appImage files"
    print "Create ~/.local/bin folder"
    
    mkdir -p ~/.local/bin
    check_return_code $?
    
    ln -sfv $(pwd)/.local/bin/git-prlink ~/.local/bin
    check_return_code $? ".git-prlink symlink"

    ln -sfv $(pwd)/.local/bin/git-filter-branch-dir ~/.local/bin
    check_return_code $? ".git-filter-branch-dir symlink"   
    
    ln -sfv $(pwd)/.local/bin/gogh ~/.local/bin
    check_return_code $? ".gogh symlink"

    cp -f $(pwd)/.local/bin/exa ~/.local/bin
    check_return_code $? ".exa copy"
    
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

    # .desktop files ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    # Configure .desktop files
    ln -sfv $(pwd)/.local/share/applications/aseprite.desktop ~/.local/share/applications
    check_return_code $? "aseprite.desktop symlink"
    
    ln -sfv $(pwd)/.local/share/applications/godot.desktop ~/.local/share/applications
    check_return_code $? "godot.desktop symlink"

    ln -sfv $(pwd)/.local/share/applications/postman.desktop ~/.local/share/applications
    check_return_code $? "postman.desktop symlink"
    
}


setup_vscode(){
    
    # Install VS Code and restore settings
    
    msg "Install VS Code and restore settings"
    new_line
        
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


setup_nodejs(){

    # Install nvm to install NodeJs
    sudo apt install curl -y
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash 
    source ~/.bashrc 

    # Install NodeJs LTS
    nvm install v14.16.0 
    
    # Install Hexo ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    npm install hexo
    
    # The $? get result of last command
    check_return_code $? "Hexo"
    
}


setup_apps(){
    
    # Install apt apps ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    new_line
    print "Installing apt Apps"
    new_line
    
    apt_apps=(
        "gpick"
        "tree"
        "neofetch"
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
        "dconf-cli"
        "uuid-runtime"
    )
    
    for app in "${apt_apps[@]}"; do
        msg_install "$app"
        
        # Install app
        sudo apt install $app -y
        
        # The $? get result of last command
        check_return_code $? $app
        
    done

    ## Install deb apps ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    msg "Installing deb packages"
    new_line
     
    msg_install "bat"
    wget https://github.com/sharkdp/bat/releases/download/v0.18.3/bat_0.18.3_amd64.deb
    sudo dpkg -i bat_0.18.3_amd64.deb
    check_return_code $?
    rm -f bat_0.18.3_amd64.deb

    
    msg_install "btm"
    wget https://github.com/ClementTsang/bottom/releases/download/0.6.4/bottom_0.6.4_amd64.deb
    sudo dpkg -i bottom_0.6.4_amd64.deb
    check_return_code $?
    rm -f bottom_0.6.4_amd64.deb
    
    # Install snap apps ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    msg "Installing Snap packages"
    new_line
    
    snap_apps=(
        "core"
        "code --classic"
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

    neofetch

}

usage() {
    
    echo "Usage:" >&2
    echo "$0 [--dotfiles] [--vscode] [--chrome] [--apps] [--dev] [--hosts]" >&2
    echo "" >&2
    echo "Options:" >&2
    echo "   --dotfiles       Symlink dotfiles in home/ directory" >&2
    echo "   --vscode         Install VsCode and symlink config" >&2
    echo "   --gchrome        Install Google Chrome" >&2
    echo "   --nodejs         Install NodeJs" >&2
    echo "   --hosts          Create local hosts files and symlink it" >&2
    echo "   --apps           Install development and general applications" >&2
    echo "   --dev            Install development libs" >&2
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
        --nodejs)
            setup_nodejs;
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
