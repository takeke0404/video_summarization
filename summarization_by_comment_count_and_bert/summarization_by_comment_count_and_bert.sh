#!/bin/sh
target="../summarization_by_bert/predict_result/*"
for filename in $target; do
    name=${filename##*/}
    name=${name%.*}
    echo "$name"
    python summarization_by_comment_count_and_bert.py "$name"
done
echo "summarization_by_comment_count_and_bert is done"
