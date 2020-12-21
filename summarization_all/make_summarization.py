import csv
import wave
import sys
import numpy as np

clip_length=300

def taple_join(taple,n):
    result = [taple[0]]
    for typet,st,et in taple:
        typer,sr,er = result[-1]
        if(sr<=st and et<=er):
            result[-1]=(typer,sr,er)
        elif(er+n>=st):
            result[-1]=(typer,sr,et)
        else:
            result.append((typet,st,et))
    return result

if __name__ == "__main__":
    name=sys.argv[1]
    predict=[]
    with open('./predict_result/'+name+'.csv') as f:
        for t,s,e,a,b in csv.reader(f):
            predict.append([t,s,e,a,b])
    predict=sorted(predict, key=lambda x: x[4],reverse=True)
    n=0
    flag=True
    clip_segments=[]
    while flag:
        n+=1
        l=predict[0:n]
        segments = []
        detect=False
        with open("./segmentation/"+name+".csv") as f:
            prev = ("",0,0)
            for type,start,end in csv.reader(f):
                if(detect):
                    if(type=="noise"):# 誤検知の可能性があるので検出直後のnoise区間は追加
                        detect=False
                        segments.append((type,float(start),float(end)))
                        continue
                    detect=False
                    continue
                for t,s,e,a,b in l:
                    if(float(e)==float(end)):
                        # 検出された区間のひとつ前のnoEnergy,noise以外の区間を結合
                        segments.append(prev)
                        # 検出された区間の結合
                        segments.append((type,float(start),float(end)))
                        detect=True
                        break
                if (type != "noEnergy" and type != "noise"):
                    prev = (type,float(start),float(end))
            segments = list(dict.fromkeys(segments))
        # 前の区間と5秒以上空いていない区間同士を結合
        segments = taple_join(segments,5)
        length=0
        for t,s,e in segments:
            length+=e-s
        if (length>clip_length):
            flag=False
        else:
            clip_segments=segments

    # urlを先頭につけてcsvで書き出し
    url=""
    with open('./name_list.txt') as f:
        for video_url,video_name in csv.reader(f):
            if(video_name==name):
                url=video_url
    with open('./result_by_bert/'+name+".csv",mode='w') as f:
        print(*url, sep='',file=f)
        for type,start,end in clip_segments:
            print(*(round(start,2),round(end,2)), sep=',', file=f)
