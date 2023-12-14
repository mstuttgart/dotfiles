#!/usr/bin/env bash

function main(raindrops) {

    res=""

    if [[ ($raindrops %  3) == 0]]; then
        $(res += "Pling")
    fi

    if [[ ($raindrops %  5) == 0]]; then
        $(res += "Plong")
    fi

    if [[ $(raindrops % 7) == 0]]

}

main "$@"
