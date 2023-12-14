#!/usr/bin/env bash

function main() {

  # if [[ $# != 2 ]]; then
  #   echo "Usage: hamming.sh <string1> <string2>"
  #   exit 1
  # fi

  # elif [[ -z "$1" ]] && [[ -z "$2" ]]; then
  #   echo "0"
  #   exit 0

  # elif [[ -z "$1" || -z "$2" ]]; then
  #   echo "strands must be of equal length"
  #   return 1

  # lenght of strands
  # if [[ ${#1} != ${#2} ]]; then
  #   echo "strands must be of equal length"
  #   exit 1

  # fi

  strand_1=$1
  strand_2=$2
  strand_len=${#strand_1}

  h_distance=0

  for ((i = 0; i < $strand_len; i++)); do

    # echo "${strand_1:i:1}"
    # echo "$i"
    #  ((h_distance += 1))

    if [[ ${strand_1:i:1} != ${strand_2:i:1} ]]; then
      ((h_distance += 1))
    fi

  done

  # echo "$h_distance"

}

main $@
