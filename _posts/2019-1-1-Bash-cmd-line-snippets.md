---
layout: post
title: Bash command line snippets
---

Searches for a file pattern and renames the part in the middle.

Tip: Use `rename -n` when first trying this out, the replace with `rename -v`.

```
avarvaruc@work-pc:~/$ find . -type f -iname '*_any_any_domestic_managed.str' -exec rename -v 's/(.)_domestic_(.)/$1_any$2/i' {} \;
./es_any_any_domestic_managed.str renamed as ./es_any_any_any_managed.str
./fr_any_any_domestic_managed.str renamed as ./fr_any_any_any_managed.str
./en_any_any_domestic_managed.str renamed as ./en_any_any_any_managed.str

```


Generate a list of keys by excluding contents of certain directories and trying to match a regex for each line.

```
find . -name any.str -not -path '*RuntimeResMSO*' -not -path '*ResHelpTroubleshooting*' -exec grep -Eo "^\[(.*)\]\s+\:\s+(STRING|STRARRAY)\s*=\s*.*$" {} \; | cut -d: -f1
```

Diplay exit status of a command

```
#!/bin/bash
# Display exit status of the command:
# echo $?

echo -n "Enter user name : "
read USR
cut -d: -f1 /etc/passwd | grep "$USR" > /dev/null
OUT=$?
if [ $OUT -eq 0 ];then
echo "User account found!"
else
echo "User account does not exists in /etc/passwd file!"
fi
```

Bash script command line arguments template

```
#!/bin/sh
## Credits to https://agateau.com/2014/template-for-shell-based-command-line-scripts/

set -e

PROGNAME=$(basename $0)

die() {
    echo "$PROGNAME: $*" >&2
    exit 1
}

usage() {
    if [ "$*" != "" ] ; then
        echo "Error: $*"
    fi

    cat << EOF
Usage: $PROGNAME [OPTION ...] [foo] [bar]
<Program description>.
Options:
-h, --help          display this usage message and exit
-d, --delete        delete things
-o, --output [FILE] write output to file
EOF

    exit 1
}

foo=""
bar=""
delete=0
output="-"
while [ $# -gt 0 ] ; do
    case "$1" in
    -h|--help)
        usage
        ;;
    -d|--delete)
        delete=1
        ;;
    -o|--output)
        output="$2"
        shift
        ;;
    -*)
        usage "Unknown option '$1'"
        ;;
    *)
        if [ -z "$foo" ] ; then
            foo="$1"
        elif [ -z "$bar" ] ; then
            bar="$1"
        else
            usage "Too many arguments"
        fi
        ;;
    esac
    shift
done

if [ -z "$bar" ] ; then
    usage "Not enough arguments"
fi

cat <<EOF
foo=$foo
bar=$bar
delete=$delete
output=$output
EOF

```
