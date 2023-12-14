#!/usr/bin/env bash

function main() {

    strand_1=$1
    strand_2=$2

    if [[ $strand_1 == "" ]] && [[ $strand_2 == "" ]]; then
        echo 0
        return 0
    fi

    if [[ -z "$1" ]] && [[ -z "$2" ]]; then
        echo "Usage: hamming.sh <string1> <string2>"
        return 1
    fi

    if [[ $strand_1 == "" ]] || [[ $strand_2 == "" ]]; then
        echo "strands must be of equal length"
        return 1
    fi

    # if [[ $# == 0 ]]; then
    #     echo "Usage: hamming.sh <string1> <string2>"
    #     return 1
    # fi

    # lenght of strands
    strand_len=${#strand_1}

    if [[ $strand_len != ${#strand_2} ]]; then
        echo "strands must be of equal length"
        return 1
    fi

    h_distance=0

    for ((i = 0; i < $strand_len; i++)); do

        if [[ ${strand_1[$i]} != ${strand_2[$i]} ]]; then
            ((h_distance += 1))
        fi

    done

    echo $h_distance

}

main $@
