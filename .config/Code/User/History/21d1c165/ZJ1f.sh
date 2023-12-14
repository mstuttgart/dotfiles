#!/usr/bin/env bash

main() {

    NUMBER="$1"

    NUMBER_LEN=${#NUMBER}

    # echo $NUMBER_LEN
    TOTAL=0

    for n in {0..$NUMBER_LEN}; do

        TOTAL+=$(${NUMBER:n:1})**

    done



}

main "$@"
