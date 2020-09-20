#!/bin/sh
while IFS=',' read a b
do
    video_id=${a##*=}
    flag=0
    comments="comments/*"
    for filename in $comments; do
        if [ "$filename" = "comments/$b.json" ]; then
            flag=1
        fi
    done
    if [ $flag -eq 1 ]; then
        echo "comments/$b.json exists"
    else
        echo "get comment $b"
        python -c "import get_comment; import sys; get_comment.get_comment_json(sys.argv[1],sys.argv[2])" $video_id "comments/$b.json"
    fi
done < ./name_list.txt
echo "get_comment is done"
