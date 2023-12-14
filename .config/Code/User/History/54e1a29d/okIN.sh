#!/bin/bash

source colors.sh

msg_install "Configurando email do git para o usuario Bot"

# Configuramos o email do bot para que possamos realizar 'push'
# e outras operações do git
# git config --global user.name "MultidadosTI Bot"
# git config --global user.email "bot@multidadosti.com.br"

# Configurando repositorio 'multierp-project'" ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

msg_install "Realizando clone do repositorio 'multierp-project'"

# Clonamos o repositorios do multierp
git clone git@github.com:multidadosti-erp/multierp-project.git multierp

msg_install "Instalando dependencias do repositorio 'multierp-project'"

cd multierp

# Criamos o virtualenv para os scripts de infra-multierp
python -p python3 .venv

# Ativamos o virtualenv
source .venv/bin/activate

# Instalamos as dependencias separadas porque nao desejamos 
#instalar todas as dependencias do odoo
pip install -e .
pip install click
pip install jinja2
pip install psycopg2-binary
pip install wheel

msg_install "Realizando download do multierp. Isso pode demorar..."

# Realizamos o download dos submodules
git submodule init
git submodule update

# Realizamos a copia das branchs main, develop e qa
manager git fetch
manager git foreach 'git checkout -t origin/main'
manager git foreach 'git checkout -t origin/develop'

# Desativamos o virtualenv
deactivate

msg_installed "'multierp-project' pronto para uso"

# Voltamos para o repositorio raiz  
cd ..

# Configurando repositorio 'infra-multierp'" ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

msg_install "Realizando clone do repositorio 'infra-multierp'"

# Clonamos o repositorios com os scripts de infra-multierp
git clone git@github.com:multidadosti-erp/infra-multierp.git infra-multierp

msg_install "Instalando dependencias do repositorio 'infra-multierp'"

cd infra-multierp

# Criamos o virtualenv para os scripts de infra-multierp
virtualenv -p python3 .venv

# Ativamos o virtualenv
source .venv/bin/activate

# Instalamos as dependencias
pip install -r requirements.txt

# Desativamos o virtualenv
deactivate

msg_installed "'infra-multierp' pronto para uso"

# Voltamos para a pasta raiz
cd ..
