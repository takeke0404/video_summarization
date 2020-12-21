#!/bin/sh
cd comments
filecount=$(ls -l | wc -l)
filecount=$((filecount - 1))
cd ../
train_num=$((filecount*7/10))
trains=$(shuf -i 1-$filecount -n $train_num)
target="./comments/*"
count=1
rm -rf test-comments/*
rm -rf train-comments/*
for filename in $target; do
    name=${filename##*/}
    if [[ $(printf '%s\n' "${trains[@]}" | grep -qx "$count"; echo -n ${?} ) -eq 0 ]];then
        cp "comments/$name" "train-comments/$name"
    else
        cp "comments/$name" "test-comments/$name"
    fi
    count=$((count + 1))
done
