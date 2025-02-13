#!/bin/sh
flag=0
MemTotal=$(grep -E '^MemTotal:' /proc/meminfo | tr -d 'MemTotal:' | tr -d 'kB')
mem_requrired_sum=0
running_list=()
while [ $flag = 0 ]
do
    while IFS=',' read a b
    do
        is_null=0
        while read c d
        do
            if [ "$d" = "$a" ]; then
                if [ "$c" = "null" ]; then
                    is_null=1
                fi
            fi
        done < ./list.txt
        if [ $is_null -eq 1 ]; then
            touch "./clip_position/$b.csv"
            continue
        fi

        if [ -f "./clip_position/$b.csv" ] || [[ $(printf '%s\n' "${running_list[@]}" | grep -qx "$b"; echo -n ${?} ) -eq 0 ]]; then
            :
        else
            mem_free=$(cat /proc/meminfo | grep MemAvailable | awk '{print $2}')
            mem_requrired=$(( $(ls -hl --block-size=K -R './videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R './clips' | grep "$b" | awk '{print $5}' | tr -d 'K')*2 ))
            mem_requrired=$(($mem_requrired*2))
            mem_requrired_temp=$(( $mem_requrired_sum+$mem_requrired ))
            if [ $mem_requrired_temp -lt $MemTotal ]; then
                bash get_clip_position.sh "$a" "$b" > /dev/null &
                running_list+=("$b")
                mem_requrired_sum=$(( $mem_requrired_sum+$mem_requrired ))
            fi
        fi
    done < ./name_list.txt

    list_size=${#running_list[@]}
    flag2=1
    while IFS=',' read a b
    do
        if [ -f "./clip_position/$b.csv" ]; then
            for ((i = 0; i < ${#running_list[@]}; i++)); do
                if [ "${running_list[$i]}" = "$b" ]; then
                    unset running_list[$i]
                    mem_requrired=$(( $(ls -hl --block-size=K -R './videos' | grep "$b" | awk '{print $5}' | tr -d 'K') + $(ls -hl --block-size=K -R './clips' | grep "$b" | awk '{print $5}' | tr -d 'K')*2 ))
                    mem_requrired=$(($mem_requrired*2))
                    mem_requrired_sum=$(( $mem_requrired_sum-$mem_requrired ))
                    echo "$b is done"
                    break
                fi
            done
        else
            flag2=0
        fi
    done < ./name_list.txt
    if [ $flag2 = 1 ]; then
        flag=1
    fi

    temp_list=()
    for ((i = 0; i < $list_size; i++)); do
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
    sleep 20
done
echo "get_clip_position is done"
