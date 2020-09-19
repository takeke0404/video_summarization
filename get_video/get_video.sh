#!/bin/sh
videos="videos/*"
videolist=()
for filename in $videos; do
    videolist+="$filename"
done
while read a b
do
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format mp3 --no-post-overwrites $b -o "videos/%(title)s.%(ext)s"
    name=""
    for filename in $videos; do
        if [[ $(printf '%s\n' "${videolist[@]}" | grep -qx "$filename"; echo -n ${?} ) -eq 0 ]]; then
            :
        else
            name="$filename"
        fi
    done
    videolist+="$name"
    name=${name##*/}
    name=${name%.*}
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format mp3 --no-post-overwrites $a -o "crips/$name.%(ext)s"
done < ./list.txt
