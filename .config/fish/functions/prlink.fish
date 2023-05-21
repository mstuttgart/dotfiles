# Show PR link in terminal
function prlink --description 'get github branch PR link'

    # get branch name
    set branch_name (git rev-parse --abbrev-ref HEAD)

    # get repository url from github
    set repo_url (git remote get-url --push origin | sed -Ee 's#(git@|git://)#https://#' -e 's@com:@com/@' -e 's%\.git$%%'  -e 's%\.git$%%' | awk '/github/')

    # Print Pull Request create link
    echo $repo_url"/compare/"$branch_name"?expand=1";

end

