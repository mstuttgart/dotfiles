#!/usr/bin/env bash

main() {

    # disable caracter globbing
    set -f

    # save the parameter string
    TEXT="$1"

    # convert all string to uppercase
    TEXT=$(echo $TEXT | tr [:lower:] [:upper:])

    # delete ',' from string
    TEXT=$(echo $TEXT | tr -d ",")

    # delete ''s' from string
    TEXT=$(echo $TEXT | tr -d "'s")

    # delete '_' from string
    TEXT=$(echo $TEXT | tr -d "_")

    # replace '-' by ' '
    TEXT=$(echo $TEXT | tr '-' ' ')

    # Separa string a partir de espaco
    # IFS: variavel especial do shell, usada para
    # separacao de strings
    IFS=" "; ARRWORD=($TEXT); unset IFS;

    ACRON=""

    for WORD in "${ARRWORD[@]}"; do
        ACRON+="${WORD:0:1}"
    done

    echo "$ACRON"

}

main "$@"
