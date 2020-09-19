#!/bin/sh
while read a b
do
    video_id=${a##*=}
    filename_list=()
    for filename in "comments/*"; do
        filename_list+=("$filename")
    done
    if [[ $(printf '%s\n' "${filename_list[@]}" | grep -qx "comments/$b.json"; echo -n ${?} ) -eq 0 ]]; then
        :
    else
        python -c "import get_comment; get_comment.get_comment_json('$video_id','comments/$b.json')"
    fi
done < ./name_list.txt
