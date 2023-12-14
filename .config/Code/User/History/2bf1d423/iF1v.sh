#!/usr/bin/env bash

  function main () {
    # your main function code here
    if [[ "$#" == 1 ]]; then
       echo "Hello, $1"
    else
        echo "error"
        return 1
    fi
  }

  # call main with all of the positional arguments
  main "$@"
