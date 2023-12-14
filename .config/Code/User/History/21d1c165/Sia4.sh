#!/usr/bin/env bash

main() {

    NUMBER="$1"
    NUMBER_LEN=${#NUMBER}

    TOTAL=0

    for ((i = 0; i < $NUMBER_LEN; i++)); do
        # echo "${NUMBER:i:1}"

        TOTAL+=(${NUMBER:i:1} ** $NUMBER_LEN)
    done

    # for i in $(seq $NUMBER_LEN); do

    #     # TOTAL+=${NUMBER:n:1} ** $NUMBER_LEN
    #     echo "${NUMBER:i:1}"

    # done

    if [[ ]]; then
        echo true
    else
        echo false
    fi

}

main "$@"
