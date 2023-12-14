#!/usr/bin/env bash

main() {

    # convert all string to uppercase
    

    # Separa string a partir de espaco
    # IFS: variavel especial do shell, usada para
    # separacao de strings
    IFS=" "; ARRWORD=($1); unset IFS;

    ACRON=""

    for WORD in "${ARRWORD[@]}"; do
        ACRON+="${WORD:0:1}"
    done

    echo "$ACRON"

}

main "$@"
