#!/bin/sh
flag=0
MemTotal=$(grep -E '^MemTotal:' /proc/meminfo | tr -d 'MemTotal:' | tr -d 'kB')
mem_requrired_sum=0
running_list=()
while [ $flag = 0 ]
do
    while IFS=',' read a b
    do
        if [ -f "./positions/$b.csv" ] || [[ $(printf '%s\n' "${running_list[@]}" | grep -qx "$b"; echo -n ${?} ) -eq 0 ]]; then
            :
        else
            mem_free=$(cat /proc/meminfo | grep MemAvailable | awk '{print $2}')
            mem_requrired=$(( $(ls -hl --block-size=K -R '../get_video/videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R '../get_video/clips' | grep "$b" | awk '{print $5}' | tr -d 'K') ))
            mem_requrired=$(($mem_requrired*6/5))
            mem_requrired_temp=$(( $mem_requrired_sum+$mem_requrired ))
            if [ $mem_requrired_temp -lt $MemTotal ]; then
                bash get_clip_position.sh "$a" "$b" > /dev/null &
                running_list+=("$b")
                mem_requrired_sum=$(( $mem_requrired_sum+$mem_requrired ))
            fi
        fi
    done < ../get_video/name_list.txt

    flag2=1
    while IFS=',' read a b
    do
        if [ -f "./positions/$b.csv" ]; then
            for ((i = 0; i < ${#running_list[@]}; i++)); do
                if [ "${running_list[$i]}" = "$b" ]; then
                    unset running_list[$i]
                    running_list=(${running_list[@]})
                    mem_requrired=$(( $(ls -hl --block-size=K -R '../get_video/videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R '../get_video/clips' | grep "$b" | awk '{print $5}' | tr -d 'K') ))
                    mem_requrired=$(($mem_requrired*6/5))
                    mem_requrired_sum=$(( $mem_requrired_sum-$mem_requrired ))
                    echo "$b is done"
                    break
                fi
            done
            continue
        else
            flag2=0
        fi
    done < ../get_video/name_list.txt
    if [ $flag2 = 1 ]; then
        flag=1
    fi
    sleep 20
    echo "${running_list[@]}"
    echo "$mem_requrired_sum/$MemTotal"
    echo ""
done
echo "get_clip_position is done"
