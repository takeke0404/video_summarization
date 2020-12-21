#!/bin/sh
positions="./videos/*"
for filename in $positions; do
    name=${filename##*/}
    name=${name%.*}
    if [ -f "./predict_result/$name.csv" ]; then
        echo "./predict_result/$name.csv exists"
        python make_summarization.py "$name"
    else
        python make_data.py "$name"
        python predict.py "$name"
        python make_summarization.py "$name"
    fi
done
echo "summarization_by_bert is done"
