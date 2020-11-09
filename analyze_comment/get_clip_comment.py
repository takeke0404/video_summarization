import json
import os
import sys
import csv

def main(comment_file):
    print("LOAD", comment_file)
    comments_json = json.load(open(comment_file, "r", encoding="UTF-8"))
    comment_file_name = os.path.splitext(os.path.basename(comment_file))[0]

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    # 範囲のコメントをファイル出力
    clip_comment = []
    with open("../get_clip_position/positions/"+comment_file_name+".csv") as f:
        for row in csv.reader(f):
            a,b = row
            for comment in comments_list:
                time,text = comment
                if( time>int(int(a)/48000) and time<int(int(b)/48000) ):
                    clip_comment.append((time,text))
    with open('comments/'+comment_file_name+".txt",mode='w') as f:
        for row in clip_comment:
            print(*row, sep=',', file=f)

def time2sec(time_str):
    sec = 0
    if time_str.startswith("-"):
        ts = time_str[1 : ]
        mul = - 1
    else:
        ts = time_str
        mul = 1
    l = ts.split(":")
    for a in l[::-1]:
        sec += int(a) * mul
        mul *= 60
    return sec

if __name__ == "__main__":
    args = sys.argv
    main(args[1])
