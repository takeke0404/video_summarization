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
            mem_requrired=$(( $(ls -hl --block-size=K -R '../get_video/videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R '../get_video/clips' | grep "$b" | awk '{print $5}' | tr -d 'K')*2 ))
            mem_requrired=$(($mem_requrired*3/2))
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
                IFS="\n"
                if [ "${running_list[$i]}" = "$b" ]; then
                    running_list[$i] = ""
                    mem_requrired=$(( $(ls -hl --block-size=K -R '../get_video/videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R '../get_video/clips' | grep "$b" | awk '{print $5}' | tr -d 'K')*2 ))
                    mem_requrired=$(($mem_requrired*3/2))
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
    temp_list=()
    for ((i = 0; i < ${#running_list[@]}; i++)); do
        if [ -n "${running_list[$i]}" ]; then
            temp_list+=("${running_list[$i]}")
        fi
    done
    running_list=("${temp_list[@]}")
    for ((i = 0; i < ${#running_list[@]}; i++)); do
        echo "${running_list[$i]}"
    done
    echo "$mem_requrired_sum/$MemTotal"
    echo ""
done
echo "get_clip_position is done"
