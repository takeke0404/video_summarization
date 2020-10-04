#!/bin/sh
videos="videos/*"
videolist=()
for filename in $videos; do
    videolist+=("$filename")
done
while read a b
do
    flag=0
    while IFS=',' read c d
    do
        if [ "$c" = "$b" ]; then
            flag=1
        fi
    done < name_list.txt
    if [ $flag -eq 1 ]; then
        echo "$b exists"
        continue
    fi
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format wav --no-post-overwrites $b -o "videos/%(title)s.%(ext)s"
    name=""
    for filename in $videos; do
        if [[ $(printf '%s\n' "${videolist[@]}" | grep -qx "$filename"; echo -n ${?} ) -eq 0 ]]; then
            :
        else
            name=("$filename")
        fi
    done
    ffmpeg -y -i "$name" -ar 48000 -ac 1 "videos/output.wav" > /dev/null
    yes | mv "videos/output.wav" "$name"
    videolist+=("$name")
    name=${name##*/}
    name=${name%.*}
    chmod 777 "videos/$name.wav"
    youtube-dl -x --extract-audio --audio-quality 0 --audio-format wav --no-post-overwrites $a -o "clips/$name.%(ext)s"
    ffmpeg -y -i "clips/$name.wav" -ar 48000 -ac 1 "clips/output.wav" > /dev/null
    yes | mv "clips/output.wav" "clips/$name.wav"
    chmod 777 "clips/$name.wav"
    echo "$b,$name" >> name_list.txt
done < ./list.txt
chmod 777 name_list.txt
chmod 777 videos
echo "get_video is done"
