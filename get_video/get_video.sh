#!/bin/sh
videos="videos/*"
videolist=()
for filename in $videos; do
    videolist+="$filename"
done
name_list=()
prv_video_list=()
while read a b
do
    if [[ $(printf '%s\n' "${prv_video_list[@]}" | grep -qx "$b"; echo -n ${?} ) -eq 0 ]]; then
        continue
    fi
    prv_video_list+="$b"
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format wav $b -o "videos/%(title)s.%(ext)s"
    name_list+="$b "
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
    name_list+="$name"
    name_list+=$'\n'
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format wav $a -o "crips/$name.%(ext)s"
done < ./list.txt
echo $name_list > name_list.txt
