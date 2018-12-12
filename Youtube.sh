#!/bin/sh
TITLE=$(youtube-dl --extract-audio --output "%(title)s.%(ext)s" --quiet --exec "echo '{}'" "$1" 2>/dev/null)
if [ $? -eq 0 ] ; then
    MVTITLE="$TITLE"
    I="0"
    while [ -e "data/$MVTITLE" ] ; do
        I="$((I+1))"
        MVTITLE="$I$TITLE"
    done
    mv "$TITLE" "data/$MVTITLE"
    echo -n "$MVTITLE"
    exit 0
fi
exit 1
