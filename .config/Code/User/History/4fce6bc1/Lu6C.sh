compare_strings() {
    local string1=$1
    local string2=$2
    local diff_char=0
    
    for (( i=0; i<${#string1}; i++ )); do
        char1="${string1:i:1}"
        char2="${string2:i:1}"

        if [[ "$char1" != "$char2" ]]; then
            ((diff_char++))
        fi
    done

    echo "$diff_char"
}

no_of_args="$#"

if [[ "$no_of_args" -ne 2 ]]; then
    echo "Usage: hamming.sh <string1> <string2>"
    exit 1
elif [[ -z "$1" && -z "$2" ]]; then
    echo "0"
    exit 0
elif [[ -z "$1" || -z "$2" || ${#1} -ne ${#2} ]]; then
    echo "strands must be of equal length"
    exit 1
else
    compare_strings $1 $2
fi
