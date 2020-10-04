#!/bin/sh
while IFS=',' read a b
do
    video_id=${a##*=}
    if [ -f "./comments/$b.json" ]; then
        echo "comments/$b.json exists"
    else
        echo "get comment $b"
        python -B -c "import get_comment; import sys; get_comment.get_comment_json(sys.argv[1],sys.argv[2])" $video_id "comments/$b.json"
        chmod 777 "comments/$b.json"
    fi
done < ./name_list.txt
chmod 777 comments
echo "get_comment is done"
