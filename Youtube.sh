#!/bin/sh
TITLE=$(youtube-dl --extract-audio --quiet --exec "echo {}" "$1" 2>/dev/null)
MVTITLE="$TITLE"
I="0"
while [ -e "data/$MVTITLE" ] ; do
    I="$((I+1))"
    MVTITLE="$I$TITLE"
done
mv "$TITLE" "data/$MVTITLE"
echo -n "$MVTITLE"
exit 0
