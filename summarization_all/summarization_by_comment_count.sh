#!/bin/sh
positions="./videos/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    python summarization_by_comment_count.py "$name"
done
echo "summarization_by_comment_count is done"
