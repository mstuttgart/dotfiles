#!/usr/bin/env bash

function main() {

    res=""
    raindrop=$1

    if [[ $((raindrop % 3)) == 0 ]]; then
        res+="Pling"
    fi

    if [[ $((raindrop % 5)) == 0 ]]; then
        res+="Plang"
    fi

    if [[ $((raindrop % 7)) == 0 ]]; then
        res+="Plong"
    fi

    if [[ "${#res}" == 0 ]]; then
        echo "$raindrop"
    else
        echo "$res"
    fi

}

main "$@"
