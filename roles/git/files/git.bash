#!/bin/bash

# Show PR link in terminal
prlink() {
    branch_name=`git rev-parse --abbrev-ref HEAD`

    repo_url=`git remote get-url --push origin | sed -Ee 's#(git@|git://)#https://#' -e 's@com:@com/@' -e 's%\.git$%%'  -e 's%\.git$%%' | awk '/github/';`

    # Print Pull Request create link
    echo $repo_url"/compare/"$branch_name"?expand=1";
}

# Clean repository and keep the folder history only
filterdir() {
    MODULE_NAME=$1;
    git filter-branch --subdirectory-filter ${MODULE_NAME} -f;
    git filter-branch -f --tree-filter 'mkdir -v '"$MODULE_NAME"'; git mv -k * '"$MODULE_NAME"'' HEAD;
}