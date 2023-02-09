![dotfiles](https://user-images.githubusercontent.com/8174740/217931237-89c965a2-bb7c-4dd2-a878-14e0296011ab.png)

<p align="center">
  <a href="https://travis-ci.org/mstuttgart/dotfiles">
    <img src="https://img.shields.io/travis/mstuttgart/dotfiles/master.svg?style=for-the-badge&color=bed5c5" alt="Build">
  </a>
  <a href="https://github.com/mstuttgart/dotfiles">
    <img src="https://img.shields.io/badge/OS-Linux-informational?style=for-the-badge&logo=linux&logoColor=white&color=bed5c5" alt="License">
  </a>
  <a href="https://github.com/mstuttgart/dotfiles">
    <img src="https://img.shields.io/badge/Tools-Ansible-informational?style=for-the-badge&logo=ansible&logoColor=white&color=bed5c5" alt="License">
  </a>
  <a href="https://github.com/mstuttgart/dotfiles/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/mstuttgart/dotfiles.svg?style=for-the-badge&color=bed5c5" alt="License">
  </a>
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#install">Install</a> |
  <a href="#credits">Credits</a>
</p>

## About

This repository serves as my way to help me setup and maintain my Ubuntu (version 20.04 LTS). 

**Warning**: Settings applied by this repository are very personal, and definitely not suite everyones needs. I suggest to create or fork your own set of dotfiles based on this repo.

## Install

Clone this repo. You can clone it in your /home folder, for example.

```
git clone git@github.com:mstuttgart/dotfiles.git ~/.dotfiles
```

or download it from link: [download](https://github.com/mstuttgart/dotfiles/archive/refs/heads/main.zip).

Install `ansible`:

```
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible
```

The `bin/setup.sh` script automatize the setup of my workstation installing all tools that I use in my setup.

```
./bin/setup.sh
```

To install separate tools, use the command with role name.


```
./bin/setup.sh rolename
```

Example:


```
./bin/setup.sh chrome
```

## Credits

Copyright (C) 2019-2023 by Michell Stuttgart
