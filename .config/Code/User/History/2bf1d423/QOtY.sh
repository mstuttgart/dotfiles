#!/usr/bin/env bash

  main () {
    # your main function code here
    if [[ "$#@" ]]; then
       echo "sucess"
    else
        

    fi
  }

  # call main with all of the positional arguments
  main "$@"
