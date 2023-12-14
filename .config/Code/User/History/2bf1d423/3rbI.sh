#!/usr/bin/env bash

  main () {
    # your main function code here
    if [[ "$#@" ]]; then
       echo "sucess"
    else
        echo "error"
        return 1
    fi
  }

  # call main with all of the positional arguments
  main "$@"
