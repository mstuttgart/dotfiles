#!/usr/bin/env bash

function main() {

    res=""

    if [[ $($1 %  3) == 0]]; then
        $(res += "Pling")
    fi

    if [[ $($1 %  5) == 0]]; then
        $(res += "Plong")
    fi

    if [[ $($1 % 7) == 0]]; then
        $(res += "Plong")

    if [[ "${#res}" == 0 ]]; then
        echo $1
    fi

}

main "$@"
