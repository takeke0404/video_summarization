import json
import os
import sys
import csv

def main(comment_file):
    print("LOAD", "../get_video/comments/"+comment_file+".json")
    comments_json = json.load(open("../get_video/comments/"+comment_file+".json", "r", encoding="UTF-8"))
    comment_file_name = os.path.splitext(os.path.basename(comment_file))[0]

    # 時刻と内容の抽出
    comments_list = []
    for comment in comments_json:
        comments_list.append((time2sec(comment["time"]), comment["text"]))

    data = []
    with open("../speech_segmentation/segmentation/"+comment_file_name+".csv") as f:
        for type,start,end in csv.reader(f):
            data.append(("noEnergy",0,0,""))
            for time,text in comments_list:
                if( float(start)+10<time and time<float(end)+10 ):
                    a,s,e,t = data.pop(-1)
                    t += text.replace(',','').replace("　","")
                    data.append((type,start,end,t))

    with open('./data/'+comment_file_name+".csv",mode='w') as f:
        for row in data:
            type,start,end,text=row
            if(text!=""):
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
