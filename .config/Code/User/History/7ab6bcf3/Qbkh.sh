#!/usr/bin/env bash

function main() {

    res=""
    raindrop=$1

    if [[ $((raindrop % 3)) == 0 ]]; then
        res+="$res"Pling
    fi

    if [[ $((raindrop %  5)) == 0 ]]; then
        res+="$res"Plang
    fi

    if [[ $((raindrop % 7)) == 0 ]]; then
        res+="$res"Plong
    fi

    if [[ "${#res}" == 0 ]]; then
        echo $1
    else
        echo "$res"
    fi

}

main "$@"
