#!/usr/bin/env bash

function main() {

    if [[ $1 ]]; then
        echo "One for $1, one for me."
    else
        echo "One for you, one for me."
    fi

}

main "$@"
