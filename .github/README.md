<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles/">
    <img src="dotfiles.png" alt="dotfiles" style="max-width:80%;height:auto;">
  </a>
</p>

## About

This repository contains my personal dotfiles and small helper scripts to set up and maintain a Linux Mint 22 (Cinnamon) workstation. It captures my preferences for shell, terminal, utilities and editor so I can quickly reproduce a working development setup.

Screenshot (example):

![Screenshot from 2024-11-03 14-31-57](https://github.com/user-attachments/assets/98905a99-dd9e-42ec-99a5-9ae0f5ecbdb4)

Key components

- OS: Linux Mint 22 Cinnamon
- Shell: zsh
  - pure — minimal, fast prompt
  - zplug — zsh plugin manager
  - zsh-syntax-highlighting — syntax highlighting
  - zsh-autosuggestions — inline suggestions
  - zsh-z — directory jumping
  - zsh-autopair — auto-close delimiters
  - asdf, fzf, virtualenvwrapper (via Oh-My-Zsh plugins)
- Terminal: Alacritty
  - tig, bat, fzf, eza, btop (recommended CLI tools)
- Editor: Neovim (my config lives in https://github.com/mstuttgart/nvim)

## Table of contents

- About
- Quick setup
- Clone & bootstrap
- Notes & caution
- Contributing
- License

## Quick setup

These steps assume a fresh-ish Linux Mint system. They only show the high-level commands — read them before running.

1. Install prerequisites (requires sudo):

```sh
sudo apt update
sudo apt install -y git yadm
```

2. Clone the repo using yadm:

```sh
yadm clone git@github.com:mstuttgart/dotfiles.git --no-bootstrap
```

If you prefer HTTPS instead of SSH:

```sh
yadm clone https://github.com/mstuttgart/dotfiles.git --no-bootstrap
```

3. If you have existing dotfiles that conflict, you can reset to this branch (this will overwrite tracked files):

```sh
# reset tracked files to the linux-mint-22 branch on origin
yadm reset --hard origin/linux-mint-22
```

4. Install or update external configs (example: Neovim config):

```sh
# clone Neovim configuration into ~/.config/nvim
git clone git@github.com:mstuttgart/nvim.git ~/.config/nvim
```

5. Run the bootstrap to install tools and apply settings (this script is provided by the repo):

```sh
yadm bootstrap
```

Read the output from the bootstrap script and follow any manual steps it prints.

## Notes & caution

- CAUTION: These are my personal settings and opinions. They may overwrite your existing configuration and may not be suitable for every environment. Review scripts (especially `yadm bootstrap`) before running.
- If you prefer to test first, inspect repository files and copy selected dotfiles manually instead of running the full bootstrap.
- The repository assumes use of zsh as the interactive shell and that you are comfortable installing tools via apt and Git.

## Contributing

This repository is primarily for my personal use, but contributions are welcome.

- Open an issue or discussion if you find bugs or want to propose changes.
- If you send a PR, keep it focused and include a short description of the change and the motivation.

## License & contact

This repository is available under the terms of the LICENSE file in the repository root.

For questions or to reach out, open an issue on GitHub.

