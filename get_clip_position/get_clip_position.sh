#!/bin/sh
while IFS=',' read a b
do
    video_id=${a##*=}
    flag=0
    output="output/*"
    for filename in $output; do
        if [ "$filename" = "output/$b.txt" ]; then
            flag=1
        fi
    done
    if [ $flag -eq 1 ]; then
        echo "output/$b.txt exists"
    else
        echo "get clip_position $b"
        python -B -u -c "import get_clip_position; import sys; get_clip_position.get_clip_position(sys.argv[1],sys.argv[2])" "../get_video/videos/$b.wav" "../get_video/clips/$b.wav" |& tee "output/$b.txt"
        chmod 777 "output/$b.txt"
        chmod 777 "positions/$b.txt"
        chmod 777 "clips/$b.wav"
    fi
done < ../get_video/name_list.txt
echo "get_clip_position is done"
