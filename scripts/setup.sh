#!/bin/bash
sudo apt install python3-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install pip --upgrade
pip install -r requirements.txt

deactivate