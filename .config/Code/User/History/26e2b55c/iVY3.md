# Infra Multierp

[![Ansible Lint](https://github.com/multidadosti-erp/setup-linux/actions/workflows/ansible-lint.yml/badge.svg)](https://github.com/multidadosti-erp/setup-linux/actions/workflows/ansible-lint.yml)

Playsbooks Ansible para configuração de servidores de QA e produção. Estes playbooks realizam a etapa de configuração do banco de dados, preparação do ubuntu, instalação do Odoo e posterior configuração do nginx e criação do certificado SSL com certbot

## Dependencias

Instalar as dependencias basicas (ansible, ansible-galaxy)

```
pip install -r requirements.txt 
```

## Comando para encriptar variaveis

```
ansible-vault encrypt_string 'this is a plaintext string' --name 'some_string'
```

## Criando novo usuario

O comando para criação de novos usuários é:

```
ansible-playbook -i environments/ambiente  playbooks/new_user.yml -u ubuntu --extra-vars "new_user='novo_usuario'"
```
Para cada usuário criado será gerado uma chave SSH que deve ser adicionada a um usuário do Github caso seja necessário realizar o
clone de algum repositorio privado.

## Instalando o Odoo

Inicialmente devemos criar um novo usuário conforme descrito anteriormente e adicionar sua chave pública ao Github.

Feito isso, podemos executar o comando a seguir para instalação e configuração do Odoo e suas dependencias:

```
ansible-playbook -i environments/ambiente  playbooks/odoo.yml -u ubuntu --extra-vars "new_user='novo_usuario'"
```

## Adicionar novo dominio ao nginx

Basta utilizar o comando abaixo:

```
ansible-playbook -i environments/ambiente playbooks/nginx.yml -u ubuntu --extra-vars "nginx_hostname=cliente_hostname nginx_domain='cliente.com.br'"
```

Onde:

* nginx_hostname: é o hostname do cliente, a primeira palavra do dominio
* nginx_domain: é o novo dominio completo

## Instalação do Postgresql

O comando a seguir cria e configura um novo usuario no Postgresql. As variaveis de configuracao do ambiente devem estar previamente preenchidas (ver arquivos no diretorio `dbservers` dentro de cada um dos ambientes para exemplo)

```
ansible-playbook -i environments/ambiente playbooks/postgresql.yml --vault-password-file=environments/ambiente/vault.key -u ubuntu 
```

Caso seja necessário, podemos tambem instalar o `pgbouncer`.

```
ansible-playbook -i environments/ambiente playbooks/pgbouncer.yml --vault-password-file=environments/ambiente/vault.key -u ubuntu 
```
