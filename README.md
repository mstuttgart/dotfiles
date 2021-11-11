<p align="center">
  <a href="https://github.com/mstuttgart/dotfiles">
  <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/emojione/178/robot-face_1f916.png"></a>
  <h4 align="center">Ansible Setup</h4>
</p>

<p align="center">
  <a href="https://travis-ci.org/mstuttgart/dotfiles">
    <img src="https://img.shields.io/travis/mstuttgart/dotfiles/master.svg?style=for-the-badge&color=FE7D3D" alt="Build">
  </a>
  <a href="https://github.com/mstuttgart/dotfiles/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/mstuttgart/dotfiles.svg?style=for-the-badge&color=FE7D3D" alt="License">
  </a>
 <a href="https://github.com/mstuttgart/dotfiles/releases">
   <img alt="GitHub release" src="https://img.shields.io/github/tag/mstuttgart/dotfiles.svg?style=for-the-badge">
 </a>
</p>

<p align="center">
  <a href="#about">About</a> |
  <a href="#install">Install</a> |
  <a href="#credits">Credits</a>
</p>

## About

This repository serves as my way to help me setup and maintain my Linux. 

**Warning**: Settings applied by this repository are very personal, and definitely not suite everyones needs. I suggest to create or fork your own set of dotfiles based on this repo.

## Install

Clone this repo. You can clone it in your /home folder, for example.

```
git clone git@github.com:mstuttgart/dotfiles.git ~/.dotfiles
```

Install `python3` and dependencies :

```
./scripts/setup.sh
```

The `install.sh` script automatize the setup of my workstation installing all libs that I use in my setup.

```
./scripts/install.sh
```

## Credits

Copyright (C) 2019-2021 by Michell Stuttgart
