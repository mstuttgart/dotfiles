#!/usr/bin/env bash

main() {

    NUMBER="$1"
    NUMBER_LEN=${#NUMBER}

    TOTAL=0

    for ((i = 0; i < $NUMBER_LEN; i++)); do

    done

    for i in $(seq $NUMBER_LEN); do

        # TOTAL+=${NUMBER:n:1} ** $NUMBER_LEN
        echo "${NUMBER:n:1}"

    done

    # if $TOTAL == $NUMBER; then
    #     echo true
    # else
    #     echo false
    # fi

}

main "$@"
