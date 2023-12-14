#!/usr/bin/env bash

function main(raindrops) {

    res=""

    if [[ $raindrops % 3 == 0]]; then
        $(res += "Pling")
    fi

}

main "$@"
