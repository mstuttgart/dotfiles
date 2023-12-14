#!/usr/bin/env bash

function main() {

    if [[ $# -ne 2 ]]; then
        echo "Usage: $0 <string1> <string2>"
        exit 1
    fi

    if [[ ${#1} -ne ${#2} ]]; then
        echo "left and right strands must be of equal length"
        exit 1
    fi

    strand_left=$1
    strand_right=$2

    dist=0
    for i in $(seq 0 $((${#strand_left} - 1))); do
        if [[ "${strand_left:$i:1}" != "${strand_right:$i:1}" ]]; then
            ((dist++))
        fi
    done
    echo "$dist"

    # strand_1=$1
    # strand_2=$2

    # # if [[ -z "$1" ]] && [[ -z "$2" ]]; then
    # #     echo "Usage: hamming.sh <string1> <string2>"
    # #     return 1
    # # fi

    # # if [[ $strand_1 == "" ]] && [[ $strand_2 == "" ]]; then
    # #     echo 0
    # #     return 0
    # # fi

    # # if [[ $strand_1 == "" ]] || [[ $strand_2 == "" ]]; then
    # #     echo "strands must be of equal length"
    # #     return 1
    # # fi

    # if [[ $# -ne 2 ]]; then
    #     echo "Usage: hamming.sh <string1> <string2>"
    #     exit 1
    # fi

    # # lenght of strands

    # if [[ ${#1} != ${#2} ]]; then
    #     echo "strands must be of equal length"
    #     exit 1
    # fi

    # strand_len=${#strand_1}

    # h_distance=0

    # for ((i = 0; i < $strand_len; i++)); do

    #     if [[ ${strand_1[$i]} != ${strand_2[$i]} ]]; then
    #         ((h_distance += 1))
    #     fi

    # done

    # echo $h_distance

}

main $@
