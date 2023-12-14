#!/usr/bin/env bash

main() {

  if [ $# != 2 ]; then
    echo "Usage: hamming.sh <string1> <string2>"
    exit 1
  fi

  if [ ${#1} != ${#2} ]; then
    echo "strands must be of equal length"
    exit 1
  fi

  h_distance=0

  for ((i = 0; i < ${#1}; i++)); do

    if [ "${1:i:1}" != "${2:i:1}" ]; then
      ((h_distance++))
    fi

  done

  echo $h_distance

}

main "$@"
