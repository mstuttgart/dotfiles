#!/usr/bin/env bash

main() {

    IFS=' '; ARRWORD=($1); unset IFS;

    # WORD_ARRAY=("${1}")

    # echo $WORD_ARRAY

    ACRON=""

    for WORD in "${ARRWORD[@]}"; do
        ACRON+=${WORD:0:1}
    done

    echo "$ACRON"

}

main "$@"
