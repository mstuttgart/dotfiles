<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="dotfiles.png" alt="dotfiles" style="max-width:80%;height:auto;">
  </a>
</p>

## About

This repository contains my personal dotfiles and Ansible playbooks to set up and maintain a development environment on Ubuntu 24.04 LTS. It captures my preferences for shell, tools, utilities and configurations so I can quickly reproduce a consistent and productive development setup.

The setup uses **Ansible** for infrastructure-as-code provisioning and maintains dotfiles in a standard Git repository with proper `.git/` structure, allowing full use of Git tools like `tig`.

### Key Components

- **OS**: Ubuntu 24.04 LTS (only supported version)
- **Provisioning**: Ansible with modular roles
- **Shell**: ZSH
  - zplug — zsh plugin manager
  - zsh-syntax-highlighting — syntax highlighting
  - zsh-autosuggestions — inline suggestions
  - asdf — version manager
  - fzf — fuzzy finder
- **Terminal**: Alacritty
  - tig — Git log viewer
  - bat — cat with syntax highlighting
  - fzf — fuzzy file finder
  - fd — fast find alternative
  - ripgrep — fast text search
  - eza — modern ls replacement
  - btop — system monitor
- **Tools**: Docker, Git, development libraries, build tools
- **Fonts**: JetBrainsMono and SourceCodePro Nerd Fonts

## Table of Contents

- [About](#about)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Ansible Roles](#ansible-roles)
- [Adding New Dotfiles](#adding-new-dotfiles)
- [Troubleshooting](#troubleshooting)
- [Notes & Caution](#notes--caution)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

### Requirements

- Ubuntu 24.04 LTS (exactly this version - script validates it)
- Internet connection
- sudo privileges
- ~3-5GB disk space

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mstuttgart/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

2. Make bootstrap script executable:

```bash
chmod +x bootstrap.sh
```

3. Run the bootstrap script:

```bash
./bootstrap.sh
```

The script will:
- Check OS compatibility (Ubuntu 24.04 LTS)
- Update system packages
- Install minimum dependencies (git, curl, python3, pip)
- Install Ansible
- Run the main Ansible playbook

4. **After installation**, logout and login (or reboot) to apply changes:

```bash
# For shell changes to take effect
logout

# Or reboot if Docker was installed
sudo reboot
```

## Installation

### Detailed Steps

#### Step 1: Clone Repository

```bash
# Via SSH (recommended if you have SSH configured)
git clone git@github.com:mstuttgart/dotfiles.git ~/dotfiles

# Or via HTTPS
git clone https://github.com/mstuttgart/dotfiles.git ~/dotfiles

cd ~/dotfiles
```

#### Step 2: Bootstrap System

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

This will be interactive and ask for your sudo password when needed.

#### Step 3: Post-Installation

After the script completes:

1. **Logout and login** to apply shell changes (ZSH as default shell)
2. **Reboot** if Docker was installed (to use docker without sudo)
3. Configure your terminal emulator:
   - Font: JetBrainsMono Nerd Font or SourceCodePro Nerd Font
   - Review `~/.zshrc` for plugin configuration

#### Step 4 (Optional): Run Specific Roles

If you want to re-run specific installation roles:

```bash
# Install only Docker
ansible-playbook playbook.yml -t docker --ask-become-pass

# Install only fonts
ansible-playbook playbook.yml -t fonts

# Install all
ansible-playbook playbook.yml --ask-become-pass
```

## Project Structure

```
dotfiles/
├── bootstrap.sh                  # Initial bootstrap script (bash)
├── playbook.yml                  # Main Ansible playbook
├── inventory/
│   └── hosts.ini                 # Ansible inventory
├── roles/
│   ├── system/                   # Base system, packages, build tools
│   ├── shell/                    # ZSH + zplug
│   ├── docker/                   # Docker CE + plugins
│   ├── dev_tools/                # Development utilities (tig, fzf, etc)
│   ├── desktop/                  # Desktop applications
│   ├── fonts/                    # Nerd Fonts installation
│   └── dotfiles/                 # Symlink configuration files
├── dotfiles/                     # Configuration files directory
│   ├── .bashrc
│   ├── .zshrc
│   ├── .gitconfig
│   └── .config/
│       └── alacritty/
│           └── alacritty.yml
├── .github/
│   ├── README.md                 # This file
│   └── BOOTSTRAP.md              # Bootstrap documentation
└── .git/                         # Normal git repository
```

## Ansible Roles

The Ansible playbook uses modular roles for different aspects of provisioning:

### 1. **system** (requires sudo)
- Updates package cache and upgrades all packages
- Installs base CLI tools: bat, btop, eza, git, tig, wget, curl, etc.
- Installs build essentials and development libraries
- Installs Python development packages (python3-dev, pip, venv, pipx)
- Installs asdf version manager (Node.js, Ruby, etc.)
- Installs Rust toolchain

**Tags**: `system`, `packages`, `version_manager`, `rust`

### 2. **shell**
- Installs ZSH shell
- Installs zplug plugin manager
- Changes default shell to ZSH

**Tags**: `shell`, `zplug`

### 3. **docker** (requires sudo)
- Adds Docker's official GPG key and repository
- Installs Docker CE with compose and buildx plugins
- Adds user to docker group (requires logout/login)
- Enables and starts Docker service

**Tags**: `docker`

### 4. **dev_tools** (requires sudo)
- Installs Alacritty terminal emulator
- Installs Git utilities: tig, meld
- Installs productivity tools: jq, fzf, fd-find, ripgrep

**Tags**: `dev_tools`, `terminal`, `git`, `utilities`

### 5. **desktop** (requires sudo)
- Installs desktop applications: filezilla, firefox, gimp, etc.
- Installs Flatpak support
- Installs Flatpak apps: Teams for Linux, Postman

**Tags**: `desktop`, `applications`, `flatpak`

### 6. **fonts**
- Creates `~/.local/share/fonts` directory
- Clones Nerd Fonts repository
- Installs JetBrainsMono Nerd Font
- Installs SourceCodePro Nerd Font
- Updates font cache

**Tags**: `fonts`

### 7. **dotfiles**
- Creates required directories (`~/.config`, `~/.local/share`, `~/.local/bin`)
- Finds all dotfiles in `dotfiles/` directory
- Creates symlinks automatically

**Tags**: `dotfiles`

## Adding New Dotfiles

To add new configuration files to be symlinked:

1. Copy your configuration file to the `dotfiles/` directory:

```bash
# Example: adding Alacritty config
mkdir -p dotfiles/.config/alacritty
cp ~/.config/alacritty/alacritty.yml dotfiles/.config/alacritty/
```

2. Maintain the same directory structure as in `$HOME`:

```
dotfiles/
├── .bashrc                          # Links to ~/.bashrc
├── .zshrc                           # Links to ~/.zshrc
├── .gitconfig                       # Links to ~/.gitconfig
└── .config/
    └── alacritty/
        └── alacritty.yml            # Links to ~/.config/alacritty/alacritty.yml
```

3. Run the playbook again to create symlinks:

```bash
ansible-playbook playbook.yml -t dotfiles --ask-become-pass
```

## Troubleshooting

### Script fails with "Unsupported operating system"

This script is designed **only for Ubuntu 24.04 LTS**. Check your version:

```bash
cat /etc/os-release
```

If you're on a different Ubuntu version, you can:
- Upgrade to 24.04 LTS
- Modify the `check_os()` function in `bootstrap.sh` to allow your version (at your own risk)
- Manually run Ansible (requires pre-installed Ansible)

### Permission denied errors

Ensure you have sudo privileges:

```bash
sudo -l
```

The bootstrap script will prompt for your password when needed.

### Ansible playbook fails

Check the detailed log output. Common issues:

1. **Package not found**: Run `sudo apt update` manually
2. **Network errors**: Check internet connection
3. **Disk space**: Ensure sufficient space (`df -h`)
4. **Existing packages**: Most roles are idempotent and safe to re-run

### Docker without sudo still requires password

You need to logout and login for group changes to take effect:

```bash
# Logout and login
exit

# Then test
docker ps
```

### ZSH not default after login

Logout and login again, or manually switch shells:

```bash
chsh -s /bin/zsh
```

### Git/tig not working properly

If using SSH keys:

```bash
# Start SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

## Notes & Caution

⚠️ **IMPORTANT**:

- **This is a personal setup** with my opinions and preferences. It may not suit your needs.
- **Review all files** before running the bootstrap script, especially if modifying roles.
- **Backup existing configurations** before running, as symlinks will overwrite existing files.
- **The script validates Ubuntu 24.04 LTS only** - other versions will be rejected.
- **Some operations require sudo** - the script will prompt for your password.
- **Idempotency**: Most Ansible tasks are idempotent (safe to run multiple times).

### What Gets Installed

- Base development tools and libraries (~1.5GB)
- Docker CE (~500MB)
- Nerd Fonts (~200MB)
- Various CLI utilities (~500MB)
- Desktop applications (varies, ~1-2GB optional)

Total: ~3-5GB depending on what you install.

### Customization

If you want to skip certain roles:

```bash
# Skip desktop applications
ansible-playbook playbook.yml --skip-tags desktop

# Skip flatpak
ansible-playbook playbook.yml --skip-tags flatpak

# Only run system updates
ansible-playbook playbook.yml --tags system
```

## Contributing

This repository is primarily for my personal use, but contributions and discussions are welcome.

- **Found an issue?** Open an issue on GitHub
- **Want to suggest changes?** Open a discussion
- **Sending a PR?** Please:
  - Keep it focused on a single change
  - Include a description of the change and motivation
  - Test on a fresh Ubuntu 24.04 LTS installation if possible

## License & Contact

This repository is available under the terms of the [LICENSE](../LICENSE) file.

For questions, bugs, or suggestions:
- Open an [Issue](https://github.com/mstuttgart/dotfiles/issues)
- Start a [Discussion](https://github.com/mstuttgart/dotfiles/discussions)

---

**Last Updated**: September 2026  
**Tested on**: Ubuntu 24.04 LTS  
**Ansible Version**: 2.10+  
**Python Version**: 3.10+

