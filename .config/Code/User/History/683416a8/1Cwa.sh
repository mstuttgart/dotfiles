#!/bin/bash

source data/db_list.sh

for db_name in "${PRODUCAO_1_DBs[@]}"; do
    ./xmlrpc/odoo_xmlrpc.py make-backup "$db_name"
    echo
done

for db_name in "${PRODUCAO_2_DBs[@]}"; do
    ./xmlrpc/odoo_xmlrpc.py make-backup "$db_name"
    echo
done

for db_name in "${PRODUCAO_3_DBs[@]}"; do
    ./xmlrpc/odoo_xmlrpc.py make-backup "$db_name"
    echo
done

for db_name in "${PRODUCAO_4_DBs[@]}"; do
    ./xmlrpc/odoo_xmlrpc.py make-backup "$db_name"
    echo
done

for db_name in "${PRODUCAO_5_DBs[@]}"; do
    ./xmlrpc/odoo_xmlrpc.py make-backup "$db_name"
    echo
done
