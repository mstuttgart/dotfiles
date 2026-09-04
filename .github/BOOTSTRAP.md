# Bootstrap Script Documentation

## Overview

The bootstrap script is an interactive installer that sets up a complete development environment with dotfiles managed by [yadm](https://yadm.io/) (Yet Another Dotfiles Manager).

## Features

- **System Updates**: Updates Ubuntu packages to latest versions
- **Development Tools**: Installs CLI tools, build systems, compilers, and programming libraries
- **Neovim**: Latest version with comprehensive dependencies for development
- **ZSH Shell**: Advanced shell with zplug plugin manager
- **Docker**: Complete Docker CE installation with compose and buildx plugins
- **Nerd Fonts**: JetBrainsMono and SourceCodePro fonts with ligatures for terminal use
- **Version Managers**: asdf for managing multiple language versions, Rust toolchain installer
- **Desktop Applications**: Essential tools for development, design, and productivity
- **Package Managers**: Flatpak support for containerized applications

## Requirements

- **Operating System**: Ubuntu 24.04 LTS or later
- **Internet connection**: Required for downloading packages and tools
- **sudo privileges**: Needed for system-level package installation and configuration
- **yadm**: Already installed (for dotfiles management)
- **Minimum disk space**: ~3-5GB for all components (without GUI dependencies)
- **RAM**: 2GB minimum recommended (4GB+ for comfortable development)

### Supported Linux Distributions

This script is designed for **Ubuntu 24.04 LTS and later versions**:
- ✅ Ubuntu 24.04 LTS (Recommended)
- ✅ Ubuntu 26.04 LTS (when available)

The script includes OS detection and will warn if running on an unsupported distribution.

## Installation

1. Clone the dotfiles repository:
   ```bash
   yadm clone https://github.com/mstuttgart/dotfiles.git
   ```

2. Run the bootstrap script:
   ```bash
   ~/.config/yadm/bootstrap
   ```

## Usage

The script provides an interactive menu with the following options:

### 1. Update System
- Updates package lists (`apt update`)
- Upgrades installed packages (`apt upgrade`)
- Removes unnecessary packages (`apt autoremove`)

### 2. Install System Packages
Installs comprehensive development packages organized by category:

**CLI Tools:**
- `bat` - Better cat with syntax highlighting
- `btop` - Resource monitor
- `ca-certificates` - Common CA certificates
- `eza` - Modern ls replacement
- `net-tools` - Network utilities
- `p7zip`, `unrar` - Archive tools (7-Zip and RAR)
- `pass` - Password manager
- `pwgen` - Password generator
- `wget` - File downloader

**Programming Tools & Build Systems:**
- `alacritty` - GPU-accelerated terminal emulator
- `build-essential` - Essential build packages and utilities
- `cmake` - Cross-platform build system
- `curl` - Data transfer tool
- `gcc` - GNU Compiler Collection
- `git` - Distributed version control system
- `make` - Build automation tool

**Development Libraries:**
- `libssl-dev` - OpenSSL development files
- `zlib1g-dev` - Compression library development files
- `libbz2-dev` - Bzip2 library development files
- `libreadline-dev` - GNU Readline library development files
- `libsqlite3-dev` - SQLite 3 database development files
- `libncursesw5-dev` - Ncurses wide-character library development files
- `xz-utils` - XZ compression utilities
- `tk-dev` - Tcl/Tk toolkit development files
- `libxml2-dev` - XML library development files
- `libxmlsec1-dev` - XML security library development files
- `libffi-dev` - Foreign Function Interface library development files
- `liblzma-dev` - LZMA compression library development files

**Python Development:**
- `python3-dev` - Python 3 development files
- `python3-pip` - Python package installer
- `python3-venv` - Python virtual environment module
- `pipx` - Python application and library installer in isolated environments

**Git & Version Control Tools:**
- `tig` - Text-mode interface for git with interactive viewing

**Desktop Applications:**
- `filezilla` - FTP/SFTP client
- `firefox` - Web browser
- `flameshot` - Screenshot tool
- `foliate` - E-book viewer
- `font-manager` - Font management application
- `gimp` - Image editor
- `gpick` - Color picker
- `meld` - Visual diff and merge tool
- `poedit` - Gettext translator
- `transmission-gtk` - BitTorrent client

**Additional Components:**
- `asdf` - Version manager for multiple programming languages (installed separately)
- `Rust` - Systems programming language and toolchain (installed via rustup)
- **Flatpak packages** (if Flatpak is available):
  - `com.github.IsmaelMartinez.teams_for_linux` - Teams for Linux
  - `com.getpostman.Postman` - API testing platform
  - `gearlever.flatpak` - AppImage manager

### 3. Install Neovim
- Downloads latest Neovim AppImage (v0.10.2)
- Installs to `/usr/bin/nvim`
- Includes essential dependencies:
  - `ripgrep` - Fast text search
  - `fd-find` - Fast file finder
  - `fzf` - Fuzzy finder
  - `xclip` - Clipboard integration

### 4. Install Fonts
- Clones Nerd Fonts repository
- Installs JetBrainsMono Nerd Font
- Installs SourceCodePro Nerd Font
- Updates system font cache

### 5. Install ZSH
- Installs ZSH shell
- Installs zplug plugin manager
- Changes default shell to ZSH (requires logout/login)

### 6. Install Docker
- Adds Docker's official GPG key
- Configures Docker repository
- Installs Docker CE with all plugins:
  - `docker-ce`, `docker-ce-cli`
  - `containerd.io`
  - `docker-buildx-plugin`
  - `docker-compose-plugin`
- Adds user to docker group
- Enables and starts Docker service

### 7. Install All
Runs all installation options in sequence:
1. Update System
2. Install System Packages
3. Install Neovim
4. Install Fonts
5. Install ZSH
6. Install Docker


## Logging

All operations are logged to timestamped files in `/tmp/`:
```
/tmp/bootstrap-YYYYMMDD-HHMMSS.log
```

The log file location is displayed at the start of the script.

## Error Handling

The script includes comprehensive error handling:
- Checks for command existence before use
- Validates OS compatibility
- Graceful failure handling with informative messages
- Automatic cleanup on exit

## Post-Installation

After running the bootstrap script:

1. **Logout and login** to apply shell and group changes (especially for ZSH and Docker)
2. **Reboot** if Docker was installed to use it without sudo
3. **Configure ZSH**: Restart terminal to load zplug plugins and configuration
4. **Font Configuration**: Set JetBrainsMono or SourceCodePro in your terminal preferences

## Customization

To customize the bootstrap script:

1. Edit package lists in the respective functions
2. Modify version numbers (e.g., Neovim version)
3. Add new installation functions following the existing pattern
4. Test on Ubuntu 24.04 LTS

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure you have sudo privileges
2. **Package not found**: Update package lists first
3. **Network issues**: Check internet connection
4. **Disk space**: Ensure sufficient disk space for all packages

### Log Analysis

Check the log file for detailed error information:
```bash
tail -f /tmp/bootstrap-YYYYMMDD-HHMMSS.log
```

### Manual Recovery

If the script fails partially:
1. Check which packages were successfully installed
2. Re-run specific menu options as needed
3. Most functions are idempotent (safe to run multiple times)

## Contributing

To contribute improvements:
1. Follow the existing code style and documentation patterns
2. Test on clean Ubuntu 24.04 LTS systems
3. Update this documentation for any new features
4. Ensure proper error handling and logging

## Deprecated/Removed Packages

The following packages have been removed from the installation list as they are no longer actively maintained or used:

- `tmux` - Terminal multiplexer (removed to simplify setup; users can install separately if needed)
- `spotify-client` - Spotify application (was available via Flatpak, no longer included by default)
- Hardware diagnostic tools (`cpu-x`, `stress-ng`, `stressapptest`, `hardinfo`) - Removed as they are specialized tools rarely needed in development environments
- `steam-installer` - Gaming platform (removed to focus on development tools)
- `default-jre` - Java runtime (can be installed separately if needed for specific projects)
- `sqlite3` - SQLite CLI (not required as `libsqlite3-dev` includes necessary components)

If you need any of these packages, you can install them manually:
```bash
sudo apt install package-name
```

Or add them to the `apt_packages` array in the bootstrap script's `install_system_packages()` function.

## License

This bootstrap script is part of the dotfiles repository and follows the same license terms.