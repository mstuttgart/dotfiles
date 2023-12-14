#!/usr/bin/env bash

function main() {
error() {
  echo "$1"
  exit 1
}
s1=$1
s2=$2
hamming=0
[[ $# -ne 2 ]] && error "Usage: hamming.sh <string1> <string2>"
[[ ${#s1} -ne ${#s2}  ]] && error "strands must be of equal length"
i=0
while [[ -n ${s1:${i}:1} ]];do
  if [[ "${s1:${i}:1}" != "${s2:${i}:1}" ]]; then
    hamming=$((hamming + 1))
  fi
  i=$((i + 1))
done
echo ${hamming}

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
